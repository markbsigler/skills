---
name: java-version-upgrade
description: Upgrade Java projects from one version to another (e.g., Java 17 to Java 21) with comprehensive dependency analysis, compatibility checking, code modernization, and framework migration (Spring Boot, Jakarta EE). Use when the user asks to upgrade Java versions, migrate to newer JDK, update Java compiler target, modernize Java codebase, update project dependencies for a new Java version, upgrade Spring Boot, or migrate from javax to jakarta packages.
---

# Java Version Upgrade

Guide Java version upgrades across projects with intelligent analysis, automated code transformation, CVE validation, and comprehensive testing.

## Key Capabilities

### 🔍 Intelligent Analysis and Upgrade Planning
Automatically analyze Java code and generate customizable upgrade plans that can be reviewed and edited. The analysis identifies:
- Current Java version and build configuration
- Spring Boot version and framework migration requirements
- Dependency compatibility issues
- Required code transformations (including javax → jakarta)
- Breaking changes and deprecated APIs
- Security vulnerabilities in current dependencies

### 🔧 Automatic Code Transformation
Execute automated code transformations using OpenRewrite to:
- Update Java syntax to modern patterns
- Migrate deprecated APIs to replacements
- Apply breaking change fixes
- Resolve build issues automatically
- Modernize code to leverage new language features

### 🛡️ Post-Upgrade CVE Validation
Scan for security vulnerabilities after upgrade:
- Detect CVE (Common Vulnerabilities and Exposures) in dependencies
- Identify code security issues
- Automatically apply security fixes
- Ensure compliance with security guidelines

### 🔄 Comprehensive Upgrade Reporting
Generate detailed summaries including:
- File changes and modifications
- Updated dependencies and versions
- Test validation results
- Remaining issues requiring manual attention

### 🧪 Unit Test Generation
Boost test coverage during upgrades:
- Generate unit tests for modified code
- Validate upgrade changes with tests
- Ensure backward compatibility

## Upgrade Workflow

Upgrading Java versions follows these phases:
1. **Analysis** - Analyze current state and plan upgrade
2. **Framework Migration** - Upgrade Spring Boot and other frameworks
3. **Transformation** - Apply automated code changes
4. **Build & Fix** - Resolve compilation and build errors
5. **Test** - Run and validate test suites
6. **CVE Check** - Scan and fix security issues
7. **Summary** - Review changes and results

## Phase 1: Analysis and Planning

### Step 1: Intelligent Code Analysis

Analyze the project to understand current state and upgrade requirements:

**Important:** Try running your application on the target JDK **before recompiling**. Most code and libraries will work without changes. This identifies runtime issues early.

```bash
# Identify current Java version and build configuration
grep -r "sourceCompatibility\|targetCompatibility" build.gradle
grep -r "<maven.compiler.source>" pom.xml
grep -r "java.version\|maven.compiler" pom.xml
```

**Run jdeps to Identify Internal API Dependencies:**

The `jdeps` tool performs static analysis to find dependencies on internal JDK APIs:

```bash
# Analyze dependencies on JDK internal APIs
jdeps -jdkinternals <your-jar-or-classes>

# Full dependency analysis with module information
jdeps --multi-release 21 -s <your-jar>

# Check specific JAR files
jdeps -jdkinternals --class-path 'libs/*' <your-jar>
```

The tool suggests replacements for internal APIs (e.g., `sun.misc.BASE64Encoder` → `java.util.Base64`).

**Note:** `jdeps` is a static analysis tool. It cannot detect internal API usage via reflection. Supplement with runtime testing.

**Run jdeprscan to Find Deprecated API Usage:**

```bash
# Scan for deprecated API usage against target version
jdeprscan --release 21 <your-jar>

# List all APIs marked for removal in target version
jdeprscan --release 21 -l --for-removal

# Scan entire project classpath
jdeprscan --release 21 --class-path 'libs/*' <your-jar>
```

Collect information about:
- Build tool (Maven/Gradle)
- Current Java version
- **Spring Boot version** (if applicable) and Spring Framework version
- All project dependencies and versions
- Plugin configurations
- Custom build scripts
- Internal JDK API dependencies (from `jdeps`)
- Deprecated API usage (from `jdeprscan`)
- javax vs. jakarta package usage

**Detect Spring Boot:**

```bash
# Check for Spring Boot in Maven
grep -r "spring-boot-starter-parent\|spring-boot-dependencies" pom.xml

# Check for Spring Boot in Gradle
grep -r "org.springframework.boot" build.gradle build.gradle.kts 2>/dev/null

# Identify current Spring Boot version
grep -r "spring-boot\|spring.boot" pom.xml build.gradle 2>/dev/null | head -5
```

**Spring Boot Version Implications:**

| Java Target | Required Spring Boot | Key Migration |
| ----------- | -------------------- | ------------- |
| Java 11 | 2.x (2.7.18 latest) | Minimal changes |
| Java 17 | 3.x (3.0+) | javax → jakarta, Spring Security 6, Hibernate 6 |
| Java 21 | 3.2+ recommended | Virtual threads support, RestClient |
| Java 25 | 4.x (planned) | Jakarta EE 11, Spring Framework 7 |

### Step 2: Run Dependency Analysis

Execute the dependency analysis script for comprehensive dependency assessment:

```bash
python scripts/analyze_java_dependencies.py --source-version <current> --target-version <target> --project-dir <path>
```

The analysis report includes:
- Dependencies requiring updates
- Known compatibility issues
- Removed JDK modules requiring explicit dependencies
- Recommended dependency versions
- Security vulnerabilities in current versions

### Step 3: Generate Upgrade Plan

Create a customizable upgrade plan document:

**Upgrade Plan Template:**
```markdown
# Java {source} → {target} Upgrade Plan

## Build Configuration Changes
- [ ] Update Maven/Gradle Java version
- [ ] Update compiler plugin versions
- [ ] Configure release flag

## Dependency Updates
- [ ] {dependency-1}: {current-version} → {target-version}
- [ ] {dependency-2}: {current-version} → {target-version}
- [ ] Add explicit dependency for {removed-module}

## Code Transformations
- [ ] Migrate javax.* to jakarta.* packages
- [ ] Replace deprecated APIs
- [ ] Apply pattern matching for instanceof
- [ ] Convert to records where applicable

## Spring Boot Migration (if applicable)
- [ ] Upgrade to latest Spring Boot 2.7.x first (stepping stone)
- [ ] Upgrade Spring Security to 5.8 bridge release
- [ ] Migrate to Spring Boot 3.x
- [ ] Migrate javax.* → jakarta.* packages
- [ ] Update Spring Boot configuration properties
- [ ] Review Spring Security 6.0 changes
- [ ] Update Spring Data/JPA for Hibernate 6.x
- [ ] Remove spring-boot-properties-migrator after completion

## OpenRewrite Recipes to Apply
- [ ] org.openrewrite.java.migrate.Java{target}
- [ ] org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0 (if Spring Boot)
- [ ] org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta
- [ ] org.openrewrite.java.dependencies.UpgradeDependencyVersion

## Testing Strategy
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance benchmarks

## CVE Remediation
- [ ] Scan for vulnerabilities
- [ ] Update vulnerable dependencies
```

Save this plan and allow the user to review and customize before proceeding.

### Step 4: Review Version-Specific Changes

Consult the migration reference for detailed information:

**See [references/java-version-changes.md](references/java-version-changes.md) for:**
- Breaking changes by version
- New features to adopt
- Deprecated APIs and replacements
- Common migration patterns
- Oracle official removed APIs by JDK version
- Charset encoding changes (UTF-8 default in JDK 18+)

**See [references/spring-boot-migration.md](references/spring-boot-migration.md) for:**
- Spring Boot and Java version compatibility matrix
- Complete Spring Boot 2.x → 3.x migration steps
- Jakarta EE package migration (javax → jakarta)
- Spring Security, Spring Batch, Spring Data changes
- Configuration property renames
- Dependency coordinate changes
- Troubleshooting common Spring Boot upgrade issues

**See [references/openrewrite-recipes.md](references/openrewrite-recipes.md) for:**
- Available OpenRewrite recipes
- Recipe configuration examples
- Spring Boot-specific OpenRewrite recipes
- Custom recipe development

### Step 5: Be Aware of Default Charset Change

Starting in JDK 18, **UTF-8 is the default charset** for all Java SE APIs on all operating systems (JEP 400). Previously, the default charset depended on the OS, locale, and encoding settings.

**Check if your environment is affected:**

```bash
# Determine the charset that was default in JDK 17 or earlier
java -XshowSettings:properties -version 2>&1 | grep native.encoding
```

If the detected encoding is not UTF-8, your application may behave differently.

**Investigation flags:**

```bash
# Test with UTF-8 on current JDK (simulates JDK 18+ behavior)
java -Dfile.encoding=UTF-8 <your-application>

# Revert to pre-JDK 18 behavior on JDK 18+ (temporary workaround)
java -Dfile.encoding=COMPAT <your-application>
```

**Common impacts:**
- File I/O with `FileReader`/`FileWriter` (no explicit charset)
- `String.getBytes()` without charset parameter
- `InputStreamReader`/`OutputStreamWriter` default constructors
- System.out/System.err on non-UTF-8 platforms

### Step 6: Compile with New --release Flag

When compiling, use the `--release` flag instead of `-source` and `-target`:

```bash
# Preferred: --release flag (ensures API compatibility)
javac --release 21 MyApp.java

# Legacy (still works but --release is better)
javac -source 21 -target 21 MyApp.java
```

The `--release` flag provides cross-compilation correctness by also restricting API access to the specified version.

**Supported --release values:** Target version down to 3 prior versions (e.g., JDK 21 supports `--release` 7 through 21).

**Important compilation notes:**
- The underscore `_` is a keyword since JDK 9 and cannot be used as an identifier
- `javac` can process class files from all prior JDK versions back to JDK 1.0.2
- Critical internal APIs like `sun.misc.Unsafe` remain accessible, but most JDK internals are not available at compile time

## Phase 2: Automated Code Transformation

### Step 1: Set Up OpenRewrite

OpenRewrite automates code transformations. Configure it in your build file:

**Maven (pom.xml):**
```xml
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.20.0</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.migrate.Java17</recipe>
            <recipe>org.openrewrite.java.migrate.JavaxToJakarta</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-migrate-java</artifactId>
            <version>2.0.0</version>
        </dependency>
    </dependencies>
</plugin>
```

**For Spring Boot projects, include the Spring recipe module:**
```xml
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.20.0</version>
    <configuration>
        <activeRecipes>
            <recipe>org.openrewrite.java.migrate.Java17</recipe>
            <recipe>org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0</recipe>
        </activeRecipes>
    </configuration>
    <dependencies>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-spring</artifactId>
            <version>5.0.0</version>
        </dependency>
        <dependency>
            <groupId>org.openrewrite.recipe</groupId>
            <artifactId>rewrite-migrate-java</artifactId>
            <version>2.0.0</version>
        </dependency>
    </dependencies>
</plugin>
```

**Gradle (build.gradle):**
```groovy
plugins {
    id 'org.openrewrite.rewrite' version '6.1.0'
}

rewrite {
    activeRecipe('org.openrewrite.java.migrate.Java17',
                 'org.openrewrite.java.migrate.JavaxToJakarta')
}

dependencies {
    rewrite('org.openrewrite.recipe:rewrite-migrate-java:2.0.0')
}
```

### Step 2: Execute Code Transformations

Run OpenRewrite to apply automated transformations:

```bash
# Maven
mvn rewrite:run

# Gradle
./gradlew rewriteRun
```

OpenRewrite will:
- Migrate package names (javax → jakarta)
- Update deprecated API usage
- Apply modern Java syntax patterns
- Fix type inference issues
- Remove unnecessary casts

**Common Recipes by Target Version:**

**Java 11:**
- `org.openrewrite.java.migrate.Java11`
- `org.openrewrite.java.migrate.JavaxActivationMigration`
- `org.openrewrite.java.migrate.JavaxXmlBindMigration`

**Java 17:**
- `org.openrewrite.java.migrate.Java17`
- `org.openrewrite.java.migrate.JavaxToJakarta`
- `org.openrewrite.java.migrate.RemovedLegacyApis`

**Java 21:**
- `org.openrewrite.java.migrate.Java21`
- `org.openrewrite.java.migrate.UpgradeToJava21`

Review the changes in version control before committing.

### Step 3: Update Build Configuration

**For Maven (pom.xml):**

Update compiler plugin and Java version properties:

```xml
<properties>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
    <java.version>21</java.version>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>21</source>
                <target>21</target>
                <release>21</release>
            </configuration>
        </plugin>
    </plugins>
</build>
```

**For Gradle (build.gradle or build.gradle.kts):**

```groovy
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

// Or using toolchain (preferred for Gradle 6.7+)
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

### Step 4: Update Dependencies

1. **Check dependency compatibility** - Review each major dependency for Java version support
2. **Update dependency versions** - Upgrade to versions compatible with target Java version
3. **Update Spring Boot** (if applicable) - Ensure Spring Boot version supports target Java

Common dependency patterns:

```xml
<!-- Spring Boot 3.x for Java 17+ -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<!-- JUnit 5 for modern testing -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
</dependency>
```

### Step 4a: Spring Boot Framework Migration

If the project uses Spring Boot, the framework upgrade is a critical parallel step. **See [references/spring-boot-migration.md](references/spring-boot-migration.md) for the complete guide.**

**Recommended Spring Boot migration order:**

```text
1. Upgrade to Spring Boot 2.7.18 (latest 2.x)
2. Upgrade Spring Security to 5.8 (bridge release)
3. Fix all 2.x deprecation warnings
4. Upgrade to Spring Boot 3.0
5. Run javax → jakarta package migration
6. Update configuration properties
7. Test and fix Spring Security 6.0 changes
8. Upgrade to latest Spring Boot 3.x (3.3+)
```

**Use the Spring Boot properties migrator** to detect renamed properties:

```xml
<!-- Add temporarily during migration -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

**Key Spring Boot 3.0 breaking changes:**

- **Jakarta EE 10**: All `javax.*` → `jakarta.*` (servlet, persistence, validation, etc.)
- **Spring Security 6.0**: New authorization model, filter dispatch changes
- **Hibernate 6.1**: New group ID (`org.hibernate.orm`), ID generation changes
- **Trailing slash matching disabled**: `/path/` no longer matches `/path`
- **Spring Batch 5.0**: `@EnableBatchProcessing` no longer needed
- **Micrometer 1.10**: Tag providers replaced by Observation conventions
- **Auto-configuration**: `spring.factories` no longer used for auto-config registration

**Enable virtual threads (Spring Boot 3.2+ with Java 21):**

```properties
spring.threads.virtual.enabled=true
```

### Step 5: Address Remaining Compatibility Issues

#### Handle Removed APIs

Java versions may remove deprecated APIs. Common removals:

**Java 11 → 17/21:**
- Removed: `javax.xml.bind` (JAXB), `javax.activation`, `java.corba`
- Solution: Add explicit dependencies or migrate to Jakarta EE

```xml
<!-- Add JAXB if needed -->
<dependency>
    <groupId>javax.xml.bind</groupId>
    <artifactId>jaxb-api</artifactId>
    <version>2.3.1</version>
</dependency>
```

**Java 17 → 21:**
- Review JEP changes and deprecations
- Check for finalized preview features now stable

#### Update Package Names

For Jakarta EE migration (Java EE → Jakarta EE):

```bash
# Find javax.* imports that need updating
grep -r "import javax\." --include="*.java" src/
```

Replace `javax.*` with `jakarta.*` where applicable:
- `javax.servlet.*` → `jakarta.servlet.*`
- `javax.persistence.*` → `jakarta.persistence.*`
- `javax.validation.*` → `jakarta.validation.*`

### Step 6: Leverage New Java Features

Adopt features from newer Java versions to improve code quality:

#### Pattern Matching (Java 17+)

**Before:**
```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
}
```

**After:**
```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

#### Records (Java 17+)

**Before:**
```java
public class Point {
    private final int x;
    private final int y;
    
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
    // getters, equals, hashCode, toString...
}
```

**After:**
```java
public record Point(int x, int y) {}
```

#### Switch Expressions (Java 17+)

**Before:**
```java
String result;
switch (day) {
    case MONDAY:
    case FRIDAY:
        result = "Work";
        break;
    case SATURDAY:
    case SUNDAY:
        result = "Rest";
        break;
    default:
        result = "Unknown";
}
```

**After:**
```java
String result = switch (day) {
    case MONDAY, FRIDAY -> "Work";
    case SATURDAY, SUNDAY -> "Rest";
    default -> "Unknown";
};
```

#### Text Blocks (Java 17+)

**Before:**
```java
String json = "{\n" +
              "  \"name\": \"John\",\n" +
              "  \"age\": 30\n" +
              "}";
```

**After:**
```java
String json = """
    {
      "name": "John",
      "age": 30
    }
    """;
```

#### Virtual Threads (Java 21+)

For high-throughput concurrent applications:

```java
// Create virtual thread
Thread.startVirtualThread(() -> {
    // task
});

// Using ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // task
    });
}
```

## Phase 4: Testing and Validation

### Step 1: Update CI/CD Configuration

Update CI/CD pipelines to use the new Java version:

**GitHub Actions:**
```yaml
- uses: actions/setup-java@v3
  with:
    distribution: 'temurin'
    java-version: '21'
```

**Jenkins:**
```groovy
tools {
    jdk 'JDK-21'
}
```

**Docker:**
```dockerfile
FROM eclipse-temurin:21-jdk-alpine
```

### Step 2: Compile and Build

Ensure the project builds successfully:

```bash
# Maven
mvn clean compile
mvn clean package

# Gradle
./gradlew clean build
```

**Address Build Errors:**

If compilation fails:
1. Review error messages for missing dependencies or API changes
2. Check if OpenRewrite missed any transformations
3. Manually fix incompatible code patterns
4. Re-run OpenRewrite with additional recipes if needed

### Step 3: Run Test Suite

Execute all tests to validate the upgrade:

```bash
# Maven
mvn test
mvn verify  # includes integration tests

# Gradle
./gradlew test
./gradlew integrationTest
```

**Test Failures:**

If tests fail:
1. Identify if failures are due to behavioral changes in new Java version
2. Update test expectations if behavior changed intentionally
3. Fix regressions in application code
4. Consider generating additional tests for modified code

### Step 4: Generate Unit Tests for Modified Code

Boost test coverage for upgraded code:

**Identify Modified Files:**
```bash
git diff --name-only HEAD~1 HEAD | grep '\.java$'
```

**For each modified file, generate tests:**

Example test generation prompt:
```
Generate comprehensive unit tests for [ClassName] that:
- Test all public methods
- Cover edge cases and error conditions
- Use modern testing patterns (JUnit 5, AssertJ)
- Achieve >80% code coverage
- Validate the behavior after Java {target} upgrade
```

**Test Frameworks:**
- **JUnit 5** - Modern test framework for Java 11+
- **AssertJ** - Fluent assertions
- **Mockito** - Mocking framework (use 4.0+ for Java 17+)

### Step 5: Performance Testing

Validate performance characteristics:

```bash
# Run performance benchmarks
mvn clean verify -P performance

# Or use JMH for micro-benchmarks
mvn clean verify -P jmh
```

Monitor:
- Application startup time
- Memory usage patterns
- Garbage collection behavior
- Throughput and latency metrics

New JVM versions often bring performance improvements, but validate there are no regressions.

## Phase 5: Security and CVE Validation

### Step 1: Scan for CVE Issues

After completing the upgrade, scan for security vulnerabilities:

**Using OWASP Dependency-Check (Maven):**
```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.4.0</version>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

```bash
mvn dependency-check:check
```

**Using Gradle:**
```groovy
plugins {
    id 'org.owasp.dependencycheck' version '8.4.0'
}
```

```bash
./gradlew dependencyCheckAnalyze
```

**Using Snyk:**
```bash
# Install Snyk CLI
npm install -g snyk

# Test for vulnerabilities
snyk test

# Monitor continuously
snyk monitor
```

### Step 2: Analyze CVE Report

Review the generated CVE report for:
- **Critical vulnerabilities** - Immediate action required
- **High severity issues** - Should be addressed
- **Medium/Low issues** - Plan for future updates
- **False positives** - Document and suppress if appropriate

### Step 3: Apply Security Fixes

For each identified vulnerability:

**1. Update Vulnerable Dependencies:**
```bash
# Maven - Update to fixed version
mvn versions:use-latest-versions -Dincludes=<groupId>:<artifactId>

# Gradle - Update in build.gradle
```

**2. Use OpenRewrite for Security Updates:**
```xml
<activeRecipes>
    <recipe>org.openrewrite.java.dependencies.UpgradeDependencyVersion</recipe>
    <recipe>org.openrewrite.java.security.SecureRandomPrefersDefaultSeed</recipe>
    <recipe>org.openrewrite.java.security.UseFilesCreateTempDirectory</recipe>
</activeRecipes>
```

**3. Address Code-Level Security Issues:**

Common issues to fix:
- Replace insecure random number generation
- Update cryptographic algorithms to modern standards
- Fix SQL injection vulnerabilities
- Address XML external entity (XXE) issues

### Step 4: Re-run Tests After Security Fixes

After applying security fixes:
```bash
mvn clean verify
./gradlew clean build test
```

Ensure all tests still pass after security updates.

## Phase 6: Summary and Documentation

### Step 1: Generate Upgrade Summary

Create a comprehensive summary document:

**Upgrade Summary Template:**
```markdown
# Java {source} → {target} Upgrade Summary
**Date:** {date}
**Duration:** {duration}
**Status:** ✅ Complete

## Files Modified
**Total:** {count} files
- Source files: {java-files}
- Test files: {test-files}
- Build files: {build-files}
- Configuration files: {config-files}

### Key Changes
- {file-1}: {description}
- {file-2}: {description}

## Dependencies Updated
**Total:** {count} dependencies

### Major Updates
| Dependency | Previous | New | Reason |
|------------|----------|-----|--------|
| {name} | {old-ver} | {new-ver} | Java {target} compatibility |
| {name} | {old-ver} | {new-ver} | CVE fix |

### Added Dependencies
- {dependency}: {reason}

## Build & Test Results
- ✅ Compilation: Success
- ✅ Unit Tests: {passed}/{total} passed
- ✅ Integration Tests: {passed}/{total} passed
- ⚠️ Failed Tests: {count} (see details below)

## CVE Scan Results
- ✅ Critical: 0
- ✅ High: 0  
- ⚠️ Medium: {count}
- ℹ️ Low: {count}

### Addressed CVEs
- CVE-{id}: {description} - Fixed by updating {dependency}

## Performance Impact
- Startup time: {before} → {after} ({percentage})
- Memory usage: {before} → {after} ({percentage})
- Throughput: {before} → {after} ({percentage})

## Code Modernizations Applied
- ✅ Pattern matching for instanceof: {count} locations
- ✅ Records: {count} classes converted
- ✅ Switch expressions: {count} conversions
- ✅ Text blocks: {count} conversions
- ✅ javax → jakarta migration: {count} files

## Remaining Issues
### Minor Issues ({count})
- [ ] {issue-1}: {description}
- [ ] {issue-2}: {description}

### Technical Debt
- [ ] Consider adopting virtual threads for {component}
- [ ] Evaluate sealed classes for {hierarchy}

## Recommendations
1. {recommendation-1}
2. {recommendation-2}

## Rollback Plan
Git tag: `pre-java-{target}-upgrade`
```

Generate this summary automatically by:
```bash
# Get file changes
git diff --stat main..upgrade-branch

# Count test results from build output
mvn surefire-report:report
```

### Step 2: Update Project Documentation

Update project documentation to reflect the upgrade:

**README.md:**
```markdown
## Requirements
- Java {target} or higher
- Maven {version} / Gradle {version}
```

**CHANGELOG.md:**
```markdown
## [{version}] - {date}
### Changed
- Upgraded from Java {source} to Java {target}
- Updated {dependency} to version {version}
- Migrated javax.* to jakarta.* packages

### Fixed  
- CVE-{id}: {description}
```

### Step 3: Commit and Tag

Commit the upgrade with a comprehensive message:

```bash
# Create upgrade branch
git checkout -b upgrade/java-{target}

# Stage all changes
git add .

# Commit with detailed message
git commit -m "Upgrade Java {source} to {target}

- Updated build configuration to Java {target}
- Migrated {count} dependencies to compatible versions
- Applied OpenRewrite transformations for API migrations
- Fixed {count} CVE issues
- Generated tests for {count} modified classes
- All tests passing ({passed}/{total})

See UPGRADE_SUMMARY.md for full details."

# Tag the upgrade
git tag -a "java-{target}-upgrade" -m "Java {target} upgrade complete"

# Push changes
git push origin upgrade/java-{target}
git push origin --tags
```

## Common Issues and Solutions

### Module System Issues (Java 9+)

If encountering module-related errors:

```bash
# Add JVM flags for opens/exports
--add-opens java.base/java.lang=ALL-UNNAMED
--add-exports java.base/sun.nio.ch=ALL-UNNAMED
```

### Illegal Reflective Access

For libraries using reflection:

```bash
# Allow specific reflection (temporary)
--add-opens java.base/java.util=ALL-UNNAMED

# Better: Upgrade library to compatible version
```

### Strong Encapsulation

Java 17+ enforces strong encapsulation. Solutions:
1. Upgrade dependencies to versions respecting module boundaries
2. Use `--add-opens` for legacy libraries (temporary)
3. Migrate to supported APIs

### Spring Boot javax → jakarta ClassNotFoundException

When upgrading Spring Boot 2.x to 3.x, `ClassNotFoundException` for `javax.*` classes is common:

```bash
# Find remaining javax dependencies
mvn dependency:tree | grep javax
./gradlew dependencies | grep javax

# Find javax imports in source code
grep -rn "import javax\." --include="*.java" src/
```

**Note:** Some `javax.*` packages are part of the JDK and do NOT change:
`javax.crypto.*`, `javax.net.*`, `javax.sql.*`, `javax.security.auth.*`, `javax.xml.parsers.*`

### Spring Security 6.0 FilterChain Errors

Spring Security 6.0 requires lambda DSL for configuration:

```java
// BEFORE (Spring Security 5.x) - .and() chaining
http.authorizeRequests()
    .antMatchers("/public/**").permitAll()
    .and()
    .httpBasic();

// AFTER (Spring Security 6.0) - lambda DSL required
http.authorizeHttpRequests(auth -> auth
        .requestMatchers("/public/**").permitAll()
        .anyRequest().authenticated())
    .httpBasic(Customizer.withDefaults());
```

### Spring Boot Trailing Slash 404 Errors

Spring Framework 6.0 disabled trailing slash matching by default. `/api/users/` no longer matches `/api/users`:

```java
// Temporary workaround
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUseTrailingSlashMatch(true);
    }
}
```

**Better:** Update client URLs or add explicit route mappings.

## Verification Checklist

- [ ] Build configuration updated (pom.xml/build.gradle)
- [ ] All dependencies compatible with target version
- [ ] Removed APIs addressed (JAXB, CORBA, etc.)
- [ ] Package names updated (javax → jakarta if needed)
- [ ] Spring Boot upgraded to compatible version (3.x for Java 17+)
- [ ] Spring Security migrated (5.x → 6.x if applicable)
- [ ] Spring Boot configuration properties renamed/updated
- [ ] spring-boot-properties-migrator removed after migration
- [ ] New language features adopted where beneficial
- [ ] CI/CD pipelines updated
- [ ] All tests passing
- [ ] Integration tests passing
- [ ] Performance validated
- [ ] Security vulnerabilities checked
- [ ] Documentation updated

## Resources

- **Version-specific changes**: See [references/java-version-changes.md](references/java-version-changes.md)
- **Dependency analysis**: Run `scripts/analyze_java_dependencies.py`
- **Migration guides**: Consult official Java release notes and JEPs

## Best Practices

### 1. Invest in Comprehensive Planning

Before starting an upgrade, thoroughly analyze the current codebase, infrastructure, and dependencies. Create a clear roadmap:

- **Inventory the codebase** - Identify all modules, services, and their Java version dependencies
- **Map the dependency graph** - Understand how libraries and frameworks interrelate
- **Assess risk areas** - Flag modules with heavy use of internal APIs, reflection, or deprecated features
- **Define success criteria** - Establish build, test, performance, and security benchmarks
- **Allocate time realistically** - Large codebases may require weeks of incremental work
- **Engage stakeholders** - Ensure team alignment on timeline, risk tolerance, and rollback procedures

### 2. Prioritize Long-Term Support (LTS) Versions

Always target LTS releases for production systems:

- **LTS versions**: Java 8, 11, 17, 21 (next LTS: 25)
- **Benefits**: Ongoing security patches, vendor support, stable APIs, community tooling
- **Avoid non-LTS in production** - Versions like 12, 13, 14, 15, 16, 18, 19, 20 receive only 6 months of support
- **Upgrade path**: Prefer stepping through LTS versions (8 → 11 → 17 → 21) rather than skipping

```
Recommended upgrade path:
  Java 8  ──→  Java 11  ──→  Java 17  ──→  Java 21
   (LTS)        (LTS)         (LTS)         (LTS)
```

Each LTS hop isolates changes, making issues easier to diagnose and fix.

### 3. Audit and Update Dependencies

Create a comprehensive dependency audit before upgrading:

- **Catalog all dependencies** - Direct and transitive, including build plugins
- **Check compatibility matrices** - Verify each library supports the target Java version
- **Update build tools first** - Ensure Maven (3.8.x+) or Gradle (7.x+/8.x+) supports the target JDK
- **Upgrade incrementally** - Update one dependency at a time when possible, testing after each
- **Handle removed modules** - Add explicit dependencies for JDK modules removed in Java 11+ (JAXB, JAX-WS, CORBA, JavaFX)
- **Watch for transitive conflicts** - Use `mvn dependency:tree` or `./gradlew dependencies` to detect version conflicts

**Key dependencies to check first:**

| Category | Key Libraries | Notes |
| -------- | ------------- | ----- |
| Framework | Spring Boot, Quarkus, Micronaut | **Spring Boot 3.x requires Java 17+; triggers javax → jakarta migration** |
| Persistence | Hibernate, MyBatis, JDBC drivers | Hibernate 6.x for Java 17+; group ID changed to `org.hibernate.orm` |
| Testing | JUnit, Mockito, AssertJ | Mockito 4.x+ for Java 17+ |
| Build | Maven Compiler Plugin, Gradle | Update plugin versions |
| Serialization | Jackson, Gson, JAXB | Jackson 2.14+ for Java 21 |
| Logging | Log4j, Logback, SLF4J | Check for CVEs in older versions |
| Security | Spring Security | **6.0 required with Spring Boot 3.x; use 5.8 bridge** |
| Database | MySQL Connector, R2DBC | **MySQL coordinates changed: mysql:mysql-connector-java → com.mysql:mysql-connector-j** |

### 4. Automate Testing and Validation

A robust testing strategy is critical for safe upgrades:

**Testing Pyramid:**

```
         ┌─────────┐
         │  E2E    │  ← Validate full workflows
        ┌┴─────────┴┐
        │Integration │  ← Verify service interactions
       ┌┴────────────┴┐
       │  Unit Tests   │  ← Catch regressions early
       └──────────────┘
```

- **Unit tests** - Achieve >80% coverage on modified code using JUnit 5 and AssertJ
- **Integration tests** - Validate database, API, and service interactions
- **End-to-end tests** - Verify complete user workflows
- **Regression tests** - Ensure existing behavior is preserved
- **Performance tests** - Benchmark critical paths with JMH

**CI/CD Pipeline Integration:**

```yaml
# GitHub Actions example
jobs:
  upgrade-validation:
    strategy:
      matrix:
        java: [17, 21]  # Test against both versions during migration
    steps:
      - uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: ${{ matrix.java }}
      - run: mvn clean verify
      - run: mvn dependency-check:check
```

Run tests against both the current and target Java versions during the migration period to catch compatibility issues early.

### 5. Refactor and Clean the Codebase

Address technical debt systematically during the upgrade:

**Address Removed APIs:**
- Replace `javax.xml.bind` (JAXB) with explicit dependencies or alternatives
- Migrate `javax.*` packages to `jakarta.*` for Jakarta EE
- Remove reliance on `sun.*` and `com.sun.*` internal JDK classes
- Replace deprecated `Unsafe` usage with VarHandle or MethodHandle APIs

**Update JVM Configuration:**
- Remove deprecated VM flags (`-XX:MaxPermSize`, `--illegal-access=permit`)
- Use `--add-opens` as a **temporary** workaround for reflection-based libraries
- Plan to eliminate `--add-opens` flags by upgrading libraries to module-aware versions
- Update GC configuration if needed (G1GC is default since Java 9, ZGC available since Java 15)

**Adopt New Language Features Incrementally:**

Start with non-critical modules and gradually expand:

```
Phase 1: Low-risk modernization
  ├── Text blocks for multi-line strings
  ├── var for local variables (Java 10+)
  └── Enhanced switch expressions (Java 14+)

Phase 2: Moderate refactoring
  ├── Records for data-carrying classes (Java 16+)
  ├── Pattern matching for instanceof (Java 16+)
  └── Sealed classes for type hierarchies (Java 17+)

Phase 3: Advanced adoption
  ├── Virtual threads for concurrent code (Java 21+)
  ├── Pattern matching for switch (Java 21+)
  └── Record patterns for deconstruction (Java 21+)
```

**Do not rewrite everything at once.** Modernize incrementally, validating at each step.

### 6. Incorporate Performance Monitoring and Observability

Integrate monitoring before, during, and after the upgrade:

**Pre-Upgrade Baselines:**
- Capture application startup time
- Record memory usage (heap sizes, GC frequency)
- Benchmark throughput and latency on critical paths
- Document GC behavior (pause times, collection counts)

**Monitoring Tools:**

| Tool | Purpose |
|------|---------|
| New Relic / Datadog | APM, distributed tracing, alerting |
| Prometheus + Grafana | Metrics collection and visualization |
| JConsole / VisualVM | JVM monitoring (heap, threads, GC) |
| JFR (Java Flight Recorder) | Low-overhead profiling (built into JDK) |
| Micrometer | Application metrics facade |

**Post-Upgrade Validation:**

```bash
# Enable Java Flight Recorder for profiling
java -XX:+FlightRecorder \
     -XX:StartFlightRecording=duration=60s,filename=upgrade.jfr \
     -jar application.jar

# Analyze with JDK Mission Control
jmc upgrade.jfr
```

- Compare post-upgrade metrics against pre-upgrade baselines
- Watch for increased GC pressure or changed pause time patterns
- Verify thread behavior (especially if adopting virtual threads)
- Monitor startup time changes
- Track CPU and memory utilization trends

**Java 21-Specific Monitoring:**
- Monitor virtual thread usage and pinning with `-Djdk.tracePinnedThreads=short`
- Track Generational ZGC metrics if enabled
- Use JFR events for virtual thread diagnostics

### 7. Additional Best Practices

- **Version control discipline** - Create a dedicated upgrade branch, tag pre-upgrade state, commit incrementally
- **Feature flags** - Use feature flags to gradually roll out Java-version-specific features
- **Canary deployments** - Deploy upgraded application to a subset of production before full rollout
- **Documentation** - Document all decisions, workarounds, and known issues during the upgrade
- **Team knowledge sharing** - Conduct team sessions on new Java features and patterns adopted
- **Rollback plan** - Always have a tested rollback strategy before deploying to production

## References

### Oracle Official Documentation
- [Oracle JDK 25 Migration Guide](https://docs.oracle.com/en/java/javase/25/migrate/getting-started.html)
- [Oracle JDK 21 Migration Guide](https://docs.oracle.com/en/java/javase/21/migrate/getting-started.html)
- [Preparing for Migration (JDK 21)](https://docs.oracle.com/en/java/javase/21/migrate/preparing-migration.html)
- [Significant Changes in JDK Releases](https://docs.oracle.com/en/java/javase/21/migrate/significant-changes-jdk-release.html)
- [Removed APIs (JDK 21)](https://docs.oracle.com/en/java/javase/21/migrate/removed-apis.html)

### Spring Boot Migration
- [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)
- [Spring Framework 6.x Upgrade Guide](https://github.com/spring-projects/spring-framework/wiki/Upgrading-to-Spring-Framework-6.x)
- [Spring Security 5.8 → 6.0 Migration](https://docs.enterprise.spring.io/spring-security/reference/6.0/migration/index.html)
- [Spring Batch 5.0 Migration Guide](https://github.com/spring-projects/spring-batch/wiki/Spring-Batch-5.0-Migration-Guide)
- [Hibernate 6.0 Migration Guide](https://docs.jboss.org/hibernate/orm/6.0/migration-guide/migration-guide.html)
- [OpenRewrite Spring Boot Recipes](https://docs.openrewrite.org/recipes/java/spring)

### Community Guides
- [Mastering Java Application Modernization](https://www.architech.ca/articles/mastering-java-application-modernization-6-practical-tips-for-success)
- [Modernizing Legacy Java Code at Scale](https://www.moderne.ai/blog/modernizing-legacy-java-code-at-scale)
- [Java Best Practices - JetBrains](https://blog.jetbrains.com/idea/2024/02/java-best-practices/)
- [VS Code Java App Modernization](https://code.visualstudio.com/docs/java/java-app-mod)
- [Java Best Practices for Developers](https://www.clariontech.com/blog/java-best-practices-for-developers)
- [Java 8 to 25: Comprehensive Guide](https://medium.com/@vishal.kr.singh/java-25-from-java-8-to-25-a-comprehensive-guide-for-developers-architects-21ffd885dcc8)
- [From Java 11 to 21: Structured Upgrade Path](https://medium.com/but-it-works-on-my-machine/from-java-11-to-21-a-safe-and-structured-upgrade-path-907c45872237)
- [Java Version Upgrade Guide](https://www.aviator.co/blog/java-version-upgrade/)
- [Google Cloud Java Best Practices](https://docs.cloud.google.com/java/docs/java-best-practices)
- [Upgrade from Java 1.8 to Java 17](https://www.hcltech.com/blogs/upgrade-from-java-1.8-to-java-17)
- [Migrating from JDK 17 to JDK 21](https://blogs.halodoc.io/migrating-from-jdk-17-to-jdk-21-an-overview-and-practical-guide/)
