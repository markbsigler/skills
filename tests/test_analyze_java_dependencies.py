"""Tests for java-version-upgrade/scripts/analyze_java_dependencies.py."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

MAVEN_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>demo</artifactId>
  <version>1.0.0</version>
  <properties>
    <maven.compiler.source>11</maven.compiler.source>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-parent</artifactId>
      <version>2.0.0</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>5.0.0</version>
    </dependency>
  </dependencies>
</project>
"""

GRADLE_BUILD = """plugins {
    id 'java'
}

sourceCompatibility = JavaVersion.VERSION_11

dependencies {
    implementation 'org.springframework:spring-core:5.3.0'
    testImplementation("org.junit.jupiter:junit-jupiter:5.9.0")
}
"""


def write_pom(project_dir: Path, content: str = MAVEN_POM) -> Path:
    project_dir.mkdir(parents=True, exist_ok=True)
    pom = project_dir / "pom.xml"
    pom.write_text(content, encoding="utf-8")
    return pom


def test_dependency_representation_equality_and_hashing(analyzer_module: Any) -> None:
    dependency = analyzer_module.Dependency("org.example", "demo", "1.2.3")
    same_name = analyzer_module.Dependency("org.example", "demo", "2.0.0")

    assert repr(dependency) == "org.example:demo:1.2.3"
    assert repr(analyzer_module.Dependency("org.example", "demo")) == "org.example:demo"
    assert dependency == same_name
    assert dependency != "org.example:demo"
    assert len({dependency, same_name}) == 1


def test_maven_detection_and_versions(analyzer_module: Any, tmp_path: Path) -> None:
    assert analyzer_module.MavenAnalyzer(tmp_path).is_applicable() is False
    assert analyzer_module.MavenAnalyzer(tmp_path).get_current_java_version() == "unknown"
    assert analyzer_module.MavenAnalyzer(tmp_path).get_dependencies() == []

    write_pom(tmp_path)
    analyzer = analyzer_module.MavenAnalyzer(tmp_path)

    assert analyzer.is_applicable() is True
    assert analyzer.get_current_java_version() == "11"

    dependencies = analyzer.get_dependencies()
    assert [dep.full_name for dep in dependencies] == [
        "org.springframework.boot:spring-boot-starter-parent",
        "org.springframework:spring-core",
    ]
    assert dependencies[0].version == "2.0.0"


def test_maven_compiler_plugin_and_java_property(analyzer_module: Any, tmp_path: Path) -> None:
    plugin_pom = """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <configuration><source>17</source></configuration>
      </plugin>
    </plugins>
  </build>
</project>
"""
    write_pom(tmp_path / "plugin", plugin_pom)
    assert analyzer_module.MavenAnalyzer(tmp_path / "plugin").get_current_java_version() == "17"

    java_property_pom = """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <properties><java.version>21</java.version></properties>
</project>
"""
    write_pom(tmp_path / "property", java_property_pom)
    assert analyzer_module.MavenAnalyzer(tmp_path / "property").get_current_java_version() == "21"


def test_maven_malformed_pom_warns(
    analyzer_module: Any, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_pom(tmp_path, "not xml")
    analyzer = analyzer_module.MavenAnalyzer(tmp_path)

    assert analyzer.get_current_java_version() == "unknown"
    assert analyzer.get_dependencies() == []
    assert "Could not parse" in capsys.readouterr().out


def test_gradle_detection_versions_and_dependencies(analyzer_module: Any, tmp_path: Path) -> None:
    (tmp_path / "build.gradle").write_text(GRADLE_BUILD, encoding="utf-8")
    analyzer = analyzer_module.GradleAnalyzer(tmp_path)

    assert analyzer.is_applicable() is True
    assert analyzer.get_current_java_version() == "11"
    assert [dep.full_name for dep in analyzer.get_dependencies()] == [
        "org.springframework:spring-core",
        "org.junit.jupiter:junit-jupiter",
    ]

    (tmp_path / "build.gradle.kts").write_text("// kts\n", encoding="utf-8")
    assert analyzer_module.GradleAnalyzer(tmp_path).build_file is not None
    assert analyzer_module.GradleAnalyzer(tmp_path).build_file.name == "build.gradle.kts"

    empty = tmp_path / "empty"
    empty.mkdir()
    missing = analyzer_module.GradleAnalyzer(empty)
    assert missing.is_applicable() is False
    assert missing.get_current_java_version() == "unknown"
    assert missing.get_dependencies() == []


def test_gradle_toolchain_and_source_compatibility(analyzer_module: Any, tmp_path: Path) -> None:
    (tmp_path / "build.gradle").write_text(
        "java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }\n",
        encoding="utf-8",
    )
    assert analyzer_module.GradleAnalyzer(tmp_path).get_current_java_version() == "21"

    (tmp_path / "build.gradle").write_text("sourceCompatibility = '17'\n", encoding="utf-8")
    assert analyzer_module.GradleAnalyzer(tmp_path).get_current_java_version() == "17"


def test_compare_versions(analyzer_module: Any, tmp_path: Path) -> None:
    analyzer = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "17")

    assert analyzer._compare_versions("1.2", "1.10") == -1
    assert analyzer._compare_versions("1.10", "1.2") == 1
    assert analyzer._compare_versions("1.0.0", "1.0.0") == 0
    assert analyzer._compare_versions("1.0", "1.0.0") == -1
    assert analyzer._compare_versions("alpha", "beta") == 0


def test_compatibility_removed_modules_and_recommendations(
    analyzer_module: Any, tmp_path: Path
) -> None:
    write_pom(tmp_path)
    analyzer = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "17")
    dependencies = analyzer.analyzer.get_dependencies()

    issues = analyzer._check_compatibility(dependencies)
    assert [issue["dependency"] for issue in issues] == [
        "org.springframework.boot:spring-boot-starter-parent:2.0.0",
        "org.springframework:spring-core:5.0.0",
    ]
    assert all(issue["severity"] == "high" for issue in issues)

    recommendations = analyzer._get_recommendations(dependencies)
    assert recommendations == [
        {
            "dependency": "org.springframework.boot:spring-boot-starter-parent",
            "current_version": "2.0.0",
            "recommended_version": "3.0.0",
            "reason": "Better Java 17 support",
        }
    ]

    java11 = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "11")
    removed = java11._check_removed_modules(dependencies)
    assert "javax.xml.bind:jaxb-api" in removed
    assert len(removed) == 4

    unknown = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "99")
    assert unknown._check_compatibility(dependencies) == []
    assert unknown._check_removed_modules(dependencies) == []
    assert unknown._get_recommendations(dependencies) == []


def test_removed_module_dependency_is_not_reported(analyzer_module: Any, tmp_path: Path) -> None:
    pom = """<project xmlns="http://maven.apache.org/POM/4.0.0">
  <dependencies>
    <dependency>
      <groupId>javax.xml.bind</groupId>
      <artifactId>jaxb-api</artifactId>
      <version>2.3.1</version>
    </dependency>
  </dependencies>
</project>
"""
    write_pom(tmp_path, pom)
    analyzer = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "11")

    removed = analyzer._check_removed_modules(analyzer.analyzer.get_dependencies())

    assert "javax.xml.bind:jaxb-api" not in removed
    assert len(removed) == 3


def test_analyze_without_build_file(analyzer_module: Any, tmp_path: Path) -> None:
    result = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "17").analyze()

    assert result == {
        "error": "No Maven (pom.xml) or Gradle (build.gradle) file found",
        "build_type": None,
    }


def test_analyze_maven_project(
    analyzer_module: Any, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_pom(tmp_path)

    result = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "17").analyze()

    assert result["build_type"] == "Maven"
    assert result["current_version"] == "11"
    assert result["target_version"] == "17"
    assert result["total_dependencies"] == 2
    assert len(result["compatibility_issues"]) == 2
    assert len(result["recommendations"]) == 1
    assert "Java Dependency Analysis Report" in capsys.readouterr().out

    overridden = analyzer_module.DependencyAnalyzer(str(tmp_path), "8", "17").analyze()
    assert overridden["current_version"] == "8"


def test_analyze_gradle_project(analyzer_module: Any, tmp_path: Path) -> None:
    (tmp_path / "build.gradle").write_text(GRADLE_BUILD, encoding="utf-8")

    result = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "17").analyze()

    assert result["build_type"] == "Gradle"
    assert result["current_version"] == "11"
    assert result["total_dependencies"] == 2


def test_print_results_output(
    analyzer_module: Any, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    analyzer = analyzer_module.DependencyAnalyzer(str(tmp_path), None, "11")
    analyzer._print_results(
        [
            {
                "dependency": "org.example:demo:1.0",
                "current_version": "1.0",
                "min_version": "2.0",
                "severity": "high",
            }
        ],
        ["javax.xml.bind:jaxb-api"],
        [
            {
                "dependency": "org.example:demo",
                "current_version": "1.0",
                "recommended_version": "2.0",
                "reason": "Better Java 11 support",
            }
        ],
    )

    output = capsys.readouterr().out
    plain = re.sub(r"\x1b\[[0-9;]*m", "", output)
    assert "Compatibility Issues (1)" in plain
    assert "Missing Dependencies for Removed JDK Modules (1)" in plain
    assert "Recommendations (1)" in plain
    assert "Critical Issues: 1" in plain

    analyzer._print_results([], [], [])
    assert "No compatibility issues found" in capsys.readouterr().out


def test_main_returns_error_when_no_build_file(
    analyzer_module: Any,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = analyzer_module.main(
        ["--target-version", "17", "--project-dir", str(tmp_path), "--json"]
    )

    assert result == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "No Maven (pom.xml) or Gradle (build.gradle) file found"


def test_main_returns_error_for_compatibility_issues(
    analyzer_module: Any,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    write_pom(tmp_path)

    result = analyzer_module.main(
        ["--target-version", "17", "--project-dir", str(tmp_path), "--json"]
    )

    assert result == 1
    output = capsys.readouterr().out
    payload = json.loads(output[output.index("{") :])
    assert len(payload["compatibility_issues"]) == 2


def test_main_json_output_and_success(
    analyzer_module: Any,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    clean_pom = MAVEN_POM.replace("2.0.0", "3.0.0").replace("5.0.0", "6.0.0")
    write_pom(tmp_path, clean_pom)

    result = analyzer_module.main(
        ["--target-version", "17", "--project-dir", str(tmp_path), "--json"]
    )

    assert result == 0
    output = capsys.readouterr().out
    payload = json.loads(output[output.index("{") :])
    assert payload["build_type"] == "Maven"
    assert payload["compatibility_issues"] == []
