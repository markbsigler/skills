#!/usr/bin/env python3
"""
Java Dependency Analyzer for Version Upgrades

Analyzes Java projects (Maven/Gradle) to identify dependencies that may need
updates when upgrading to a new Java version.
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Tuple


class Color:
    """Terminal colors for output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


# Known compatibility issues for common libraries
COMPATIBILITY_DB = {
    "11": {
        "removed_modules": [
            "javax.xml.bind:jaxb-api",
            "javax.activation:activation",
            "javax.xml.ws:jaxws-api",
            "javax.annotation:javax.annotation-api"
        ],
        "min_versions": {
            "org.springframework.boot:spring-boot-starter-parent": "2.1.0",
            "org.springframework:spring-core": "5.1.0",
            "org.hibernate:hibernate-core": "5.3.0",
            "junit:junit": "4.12",
            "org.mockito:mockito-core": "2.23.0"
        }
    },
    "17": {
        "min_versions": {
            "org.springframework.boot:spring-boot-starter-parent": "2.5.0",
            "org.springframework:spring-core": "5.3.0",
            "org.hibernate:hibernate-core": "5.4.24",
            "org.junit.jupiter:junit-jupiter": "5.7.0",
            "org.mockito:mockito-core": "3.6.0",
            "com.fasterxml.jackson.core:jackson-databind": "2.12.0"
        },
        "recommended_versions": {
            "org.springframework.boot:spring-boot-starter-parent": "3.0.0",
            "jakarta.persistence:jakarta.persistence-api": "3.0.0"
        }
    },
    "21": {
        "min_versions": {
            "org.springframework.boot:spring-boot-starter-parent": "3.0.0",
            "org.springframework:spring-core": "6.0.0",
            "org.hibernate:hibernate-core": "6.1.0",
            "org.junit.jupiter:junit-jupiter": "5.9.0",
            "org.mockito:mockito-core": "4.0.0",
            "com.fasterxml.jackson.core:jackson-databind": "2.14.0"
        },
        "recommended_versions": {
            "org.springframework.boot:spring-boot-starter-parent": "3.2.0",
            "jakarta.persistence:jakarta.persistence-api": "3.1.0"
        }
    }
}


class Dependency:
    """Represents a project dependency"""
    
    def __init__(self, group_id: str, artifact_id: str, version: str = None):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.full_name = f"{group_id}:{artifact_id}"
    
    def __repr__(self):
        version_str = f":{self.version}" if self.version else ""
        return f"{self.full_name}{version_str}"
    
    def __eq__(self, other):
        return self.full_name == other.full_name
    
    def __hash__(self):
        return hash(self.full_name)


class MavenAnalyzer:
    """Analyze Maven projects (pom.xml)"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.pom_file = project_dir / "pom.xml"
    
    def is_applicable(self) -> bool:
        return self.pom_file.exists()
    
    def get_current_java_version(self) -> str:
        """Extract current Java version from pom.xml"""
        try:
            tree = ET.parse(self.pom_file)
            root = tree.getroot()
            
            # Handle Maven namespace
            ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
            
            # Check maven.compiler.source property
            properties = root.find('m:properties', ns)
            if properties is not None:
                source = properties.find('m:maven.compiler.source', ns)
                if source is not None and source.text:
                    return source.text
                
                java_version = properties.find('m:java.version', ns)
                if java_version is not None and java_version.text:
                    return java_version.text
            
            # Check compiler plugin configuration
            build = root.find('m:build', ns)
            if build is not None:
                plugins = build.find('m:plugins', ns)
                if plugins is not None:
                    for plugin in plugins.findall('m:plugin', ns):
                        artifact = plugin.find('m:artifactId', ns)
                        if artifact is not None and artifact.text == 'maven-compiler-plugin':
                            config = plugin.find('m:configuration', ns)
                            if config is not None:
                                source = config.find('m:source', ns)
                                if source is not None and source.text:
                                    return source.text
            
        except Exception as e:
            print(f"{Color.YELLOW}Warning: Could not parse pom.xml: {e}{Color.END}")
        
        return "unknown"
    
    def get_dependencies(self) -> List[Dependency]:
        """Extract dependencies from pom.xml"""
        dependencies = []
        
        try:
            tree = ET.parse(self.pom_file)
            root = tree.getroot()
            ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
            
            # Get direct dependencies
            deps_section = root.find('m:dependencies', ns)
            if deps_section is not None:
                for dep in deps_section.findall('m:dependency', ns):
                    group = dep.find('m:groupId', ns)
                    artifact = dep.find('m:artifactId', ns)
                    version = dep.find('m:version', ns)
                    
                    if group is not None and artifact is not None:
                        dependencies.append(Dependency(
                            group.text,
                            artifact.text,
                            version.text if version is not None else None
                        ))
            
            # Get parent dependency
            parent = root.find('m:parent', ns)
            if parent is not None:
                group = parent.find('m:groupId', ns)
                artifact = parent.find('m:artifactId', ns)
                version = parent.find('m:version', ns)
                
                if group is not None and artifact is not None:
                    dependencies.append(Dependency(
                        group.text,
                        artifact.text,
                        version.text if version is not None else None
                    ))
        
        except Exception as e:
            print(f"{Color.YELLOW}Warning: Could not parse dependencies: {e}{Color.END}")
        
        return dependencies


class GradleAnalyzer:
    """Analyze Gradle projects (build.gradle or build.gradle.kts)"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.build_file = None
        
        for filename in ["build.gradle.kts", "build.gradle"]:
            candidate = project_dir / filename
            if candidate.exists():
                self.build_file = candidate
                break
    
    def is_applicable(self) -> bool:
        return self.build_file is not None
    
    def get_current_java_version(self) -> str:
        """Extract current Java version from build.gradle"""
        if not self.build_file:
            return "unknown"
        
        try:
            content = self.build_file.read_text()
            
            # Look for sourceCompatibility
            match = re.search(r'sourceCompatibility\s*=\s*["\']?(\d+)', content)
            if match:
                return match.group(1)
            
            # Look for JavaVersion
            match = re.search(r'JavaVersion\.VERSION_(\d+)', content)
            if match:
                return match.group(1)
            
            # Look for toolchain
            match = re.search(r'languageVersion\s*=\s*JavaLanguageVersion\.of\((\d+)\)', content)
            if match:
                return match.group(1)
        
        except Exception as e:
            print(f"{Color.YELLOW}Warning: Could not parse build.gradle: {e}{Color.END}")
        
        return "unknown"
    
    def get_dependencies(self) -> List[Dependency]:
        """Extract dependencies from build.gradle"""
        dependencies = []
        
        if not self.build_file:
            return dependencies
        
        try:
            content = self.build_file.read_text()
            
            # Match dependency declarations
            # Examples: implementation 'group:artifact:version'
            #           implementation("group:artifact:version")
            pattern = r'(?:implementation|api|compile|testImplementation|testCompile)\s*[(\'\"]([^:]+):([^:]+)(?::([^\'\"]+))?[)\'\"]'
            
            for match in re.finditer(pattern, content):
                group_id = match.group(1)
                artifact_id = match.group(2)
                version = match.group(3) if match.group(3) else None
                
                dependencies.append(Dependency(group_id, artifact_id, version))
        
        except Exception as e:
            print(f"{Color.YELLOW}Warning: Could not parse dependencies: {e}{Color.END}")
        
        return dependencies


class DependencyAnalyzer:
    """Main analyzer coordinating Maven and Gradle analysis"""
    
    def __init__(self, project_dir: str, source_version: str, target_version: str):
        self.project_dir = Path(project_dir).resolve()
        self.source_version = source_version
        self.target_version = target_version
        
        # Initialize analyzers
        self.maven = MavenAnalyzer(self.project_dir)
        self.gradle = GradleAnalyzer(self.project_dir)
        
        # Select appropriate analyzer
        if self.maven.is_applicable():
            self.analyzer = self.maven
            self.build_type = "Maven"
        elif self.gradle.is_applicable():
            self.analyzer = self.gradle
            self.build_type = "Gradle"
        else:
            self.analyzer = None
            self.build_type = None
    
    def analyze(self) -> Dict:
        """Run complete analysis"""
        if not self.analyzer:
            return {
                "error": "No Maven (pom.xml) or Gradle (build.gradle) file found",
                "build_type": None
            }
        
        print(f"\n{Color.BOLD}Java Dependency Analysis Report{Color.END}")
        print(f"{'=' * 70}\n")
        print(f"Project Directory: {self.project_dir}")
        print(f"Build Type: {Color.CYAN}{self.build_type}{Color.END}")
        
        # Get current version
        detected_version = self.analyzer.get_current_java_version()
        current_version = self.source_version or detected_version
        
        print(f"Current Java Version: {Color.YELLOW}{current_version}{Color.END}")
        print(f"Target Java Version: {Color.GREEN}{self.target_version}{Color.END}")
        print()
        
        # Get dependencies
        dependencies = self.analyzer.get_dependencies()
        print(f"Found {len(dependencies)} dependencies\n")
        
        # Analyze compatibility
        issues = self._check_compatibility(dependencies)
        removed = self._check_removed_modules(dependencies)
        recommendations = self._get_recommendations(dependencies)
        
        # Print results
        self._print_results(issues, removed, recommendations)
        
        return {
            "build_type": self.build_type,
            "current_version": current_version,
            "target_version": self.target_version,
            "total_dependencies": len(dependencies),
            "compatibility_issues": issues,
            "removed_modules": removed,
            "recommendations": recommendations
        }
    
    def _check_compatibility(self, dependencies: List[Dependency]) -> List[Dict]:
        """Check if dependencies meet minimum version requirements"""
        issues = []
        
        if self.target_version not in COMPATIBILITY_DB:
            return issues
        
        min_versions = COMPATIBILITY_DB[self.target_version].get("min_versions", {})
        
        for dep in dependencies:
            if dep.full_name in min_versions:
                min_version = min_versions[dep.full_name]
                if dep.version and self._compare_versions(dep.version, min_version) < 0:
                    issues.append({
                        "dependency": str(dep),
                        "current_version": dep.version,
                        "min_version": min_version,
                        "severity": "high"
                    })
        
        return issues
    
    def _check_removed_modules(self, dependencies: List[Dependency]) -> List[str]:
        """Check for dependencies on removed JDK modules"""
        removed = []
        
        if self.target_version not in COMPATIBILITY_DB:
            return removed
        
        removed_modules = COMPATIBILITY_DB[self.target_version].get("removed_modules", [])
        dep_names = {dep.full_name for dep in dependencies}
        
        for module in removed_modules:
            if module not in dep_names:
                removed.append(module)
        
        return removed
    
    def _get_recommendations(self, dependencies: List[Dependency]) -> List[Dict]:
        """Get recommended version upgrades"""
        recommendations = []
        
        if self.target_version not in COMPATIBILITY_DB:
            return recommendations
        
        recommended = COMPATIBILITY_DB[self.target_version].get("recommended_versions", {})
        
        for dep in dependencies:
            if dep.full_name in recommended:
                rec_version = recommended[dep.full_name]
                if not dep.version or self._compare_versions(dep.version, rec_version) < 0:
                    recommendations.append({
                        "dependency": dep.full_name,
                        "current_version": dep.version or "unknown",
                        "recommended_version": rec_version,
                        "reason": "Better Java " + self.target_version + " support"
                    })
        
        return recommendations
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare semantic versions. Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2"""
        try:
            parts1 = [int(x) for x in re.findall(r'\d+', v1)]
            parts2 = [int(x) for x in re.findall(r'\d+', v2)]
            
            for a, b in zip(parts1, parts2):
                if a < b:
                    return -1
                elif a > b:
                    return 1
            
            if len(parts1) < len(parts2):
                return -1
            elif len(parts1) > len(parts2):
                return 1
            
            return 0
        except:
            return 0  # Cannot compare, assume equal
    
    def _print_results(self, issues: List[Dict], removed: List[str], 
                      recommendations: List[Dict]):
        """Print analysis results to console"""
        
        # Print compatibility issues
        if issues:
            print(f"{Color.RED}{Color.BOLD}⚠ Compatibility Issues ({len(issues)}){Color.END}")
            print(f"{'-' * 70}")
            for issue in issues:
                print(f"{Color.RED}✗{Color.END} {issue['dependency']}")
                print(f"  Current: {issue['current_version']} | "
                      f"Required: {issue['min_version']} or higher")
            print()
        else:
            print(f"{Color.GREEN}✓ No compatibility issues found{Color.END}\n")
        
        # Print removed modules warnings
        if removed:
            print(f"{Color.YELLOW}{Color.BOLD}⚠ Missing Dependencies for Removed JDK Modules ({len(removed)}){Color.END}")
            print(f"{'-' * 70}")
            print(f"Java {self.target_version} removed these modules from the JDK.")
            print(f"Add explicit dependencies if your code uses them:\n")
            for module in removed:
                print(f"{Color.YELLOW}!{Color.END} {module}")
            print()
        
        # Print recommendations
        if recommendations:
            print(f"{Color.CYAN}{Color.BOLD}💡 Recommendations ({len(recommendations)}){Color.END}")
            print(f"{'-' * 70}")
            for rec in recommendations:
                print(f"{Color.CYAN}→{Color.END} {rec['dependency']}")
                print(f"  Current: {rec['current_version']} | "
                      f"Recommended: {rec['recommended_version']}")
                print(f"  Reason: {rec['reason']}")
            print()
        
        # Summary
        print(f"{Color.BOLD}Summary{Color.END}")
        print(f"{'-' * 70}")
        print(f"Critical Issues: {Color.RED}{len(issues)}{Color.END}")
        print(f"Missing JDK Module Dependencies: {Color.YELLOW}{len(removed)}{Color.END}")
        print(f"Upgrade Recommendations: {Color.CYAN}{len(recommendations)}{Color.END}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Java project dependencies for version upgrades",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze upgrade from Java 11 to 17
  %(prog)s --source-version 11 --target-version 17 --project-dir ./my-project
  
  # Auto-detect source version
  %(prog)s --target-version 21 --project-dir .
        """
    )
    
    parser.add_argument(
        '--source-version',
        type=str,
        help='Current Java version (auto-detected if not specified)'
    )
    
    parser.add_argument(
        '--target-version',
        type=str,
        required=True,
        help='Target Java version (e.g., 11, 17, 21)'
    )
    
    parser.add_argument(
        '--project-dir',
        type=str,
        default='.',
        help='Project directory containing pom.xml or build.gradle (default: current directory)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    analyzer = DependencyAnalyzer(
        project_dir=args.project_dir,
        source_version=args.source_version,
        target_version=args.target_version
    )
    
    results = analyzer.analyze()
    
    if args.json:
        print(json.dumps(results, indent=2))
    
    # Exit with error code if critical issues found
    if "error" in results:
        sys.exit(1)
    
    issues_count = len(results.get("compatibility_issues", []))
    if issues_count > 0:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
