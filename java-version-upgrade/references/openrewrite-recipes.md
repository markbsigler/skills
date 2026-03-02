# OpenRewrite Recipes for Java Upgrades

Comprehensive guide to OpenRewrite recipes for automating Java version migrations.

## Table of Contents

- [Introduction to OpenRewrite](#introduction-to-openrewrite)
- [Setup and Configuration](#setup-and-configuration)
- [Migration Recipes by Version](#migration-recipes-by-version)
- [Framework-Specific Recipes](#framework-specific-recipes)
- [Security and Dependency Recipes](#security-and-dependency-recipes)
- [Custom Recipe Development](#custom-recipe-development)

---

## Introduction to OpenRewrite

OpenRewrite is an automated refactoring tool that applies transformations to source code using recipes. It's particularly effective for:

- Large-scale API migrations
- Framework upgrades
- Security vulnerability fixes
- Code modernization
- Dependency version updates

### How OpenRewrite Works

1. **Parse** - Build accurate AST (Abstract Syntax Tree) of your code
2. **Visit** - Recipes visit and analyze the AST
3. **Transform** - Apply changes that match recipe patterns
4. **Format** - Maintain code formatting and style
5. **Write** - Output transformed code

### Key Benefits

- **Safe** - Type-aware transformations prevent breaking changes
- **Automated** - Handles thousands of files consistently
- **Customizable** - Create custom recipes for project-specific needs
- **Composable** - Combine multiple recipes for complex migrations

---

## Setup and Configuration

### Maven Setup

Add to `pom.xml`:

```xml
<project>
    <build>
        <plugins>
            <plugin>
                <groupId>org.openrewrite.maven</groupId>
                <artifactId>rewrite-maven-plugin</artifactId>
                <version>5.20.0</version>
                <configuration>
                    <activeRecipes>
                        <!-- Add recipes here -->
                        <recipe>org.openrewrite.java.migrate.Java17</recipe>
                    </activeRecipes>
                </configuration>
                <dependencies>
                    <!-- Add recipe dependencies -->
                    <dependency>
                        <groupId>org.openrewrite.recipe</groupId>
                        <artifactId>rewrite-migrate-java</artifactId>
                        <version>2.0.0</version>
                    </dependency>
                    <dependency>
                        <groupId>org.openrewrite.recipe</groupId>
                        <artifactId>rewrite-spring</artifactId>
                        <version>5.0.0</version>
                    </dependency>
                </dependencies>
            </plugin>
        </plugins>
    </build>
</project>
```

### Gradle Setup

Add to `build.gradle`:

```groovy
plugins {
    id 'java'
    id 'org.openrewrite.rewrite' version '6.1.0'
}

rewrite {
    activeRecipe(
        'org.openrewrite.java.migrate.Java17',
        'org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2'
    )
    exportDatatables = true
}

dependencies {
    rewrite(platform('org.openrewrite.recipe:rewrite-recipe-bom:2.0.0'))
    rewrite('org.openrewrite.recipe:rewrite-migrate-java')
    rewrite('org.openrewrite.recipe:rewrite-spring')
}
```

### Using rewrite.yml (Recommended)

Create `rewrite.yml` in project root for better organization:

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.example.JavaUpgrade
displayName: Java 17 to 21 Upgrade
description: Comprehensive upgrade recipe for Java 21 migration
recipeList:
  - org.openrewrite.java.migrate.Java21
  - org.openrewrite.java.migrate.JavaxToJakarta
  - org.openrewrite.java.dependencies.DependencyVulnerabilityCheck
  - org.openrewrite.java.cleanup.Cleanup
```

Then reference in build file:

```groovy
rewrite {
    activeRecipe('com.example.JavaUpgrade')
    configFile = project.getRootProject().file('rewrite.yml')
}
```

### Running OpenRewrite

```bash
# Dry run - see what would change
mvn rewrite:dryRun
./gradlew rewriteDryRun

# Apply changes
mvn rewrite:run
./gradlew rewriteRun

# Discover available recipes
mvn rewrite:discover
./gradlew rewriteDiscover
```

---

## Migration Recipes by Version

### Java 8 → 11

**Recipe:** `org.openrewrite.java.migrate.Java11`

**Transformations:**
- Migrates removed Java EE modules to standalone dependencies
- Updates deprecated API usage
- Handles URLClassLoader changes

**Additional Recipes:**

```yaml
# JAXB Migration
- org.openrewrite.java.migrate.JavaxXmlBindMigration
  
# JAX-WS Migration  
- org.openrewrite.java.migrate.JavaxXmlWsMigration

# Activation Framework
- org.openrewrite.java.migrate.JavaxActivationMigration

# Annotation APIs
- org.openrewrite.java.migrate.JavaxAnnotationMigration
```

**Configuration:**

```xml
<activeRecipes>
    <recipe>org.openrewrite.java.migrate.Java11</recipe>
    <recipe>org.openrewrite.java.migrate.JavaxXmlBindMigration</recipe>
    <recipe>org.openrewrite.java.migrate.JavaxXmlWsMigration</recipe>
</activeRecipes>
```

### Java 11 → 17

**Recipe:** `org.openrewrite.java.migrate.Java17`

**Transformations:**
- Migrates to Java 17 APIs
- Handles strong encapsulation of JDK internals
- Updates reflection patterns for sealed packages
- Adopts modern language features

**Sub-recipes Included:**

```yaml
# Automatically included in Java17 recipe
- org.openrewrite.java.migrate.UpgradeToJava17
- org.openrewrite.java.migrate.RemovedLegacyApis
- org.openrewrite.java.migrate.RemovedToolProviderConstructor
- org.openrewrite.java.migrate.RemovedFileIOFinalizeMethods
```

**Package Migration:**

```yaml
# javax → jakarta for Java EE 9+
- org.openrewrite.java.migrate.JavaxToJakarta
```

This renames:
- `javax.servlet` → `jakarta.servlet`
- `javax.persistence` → `jakarta.persistence`
- `javax.validation` → `jakarta.validation`
- `javax.ws.rs` → `jakarta.ws.rs`
- And many more...

### Java 17 → 21

**Recipe:** `org.openrewrite.java.migrate.Java21`

**Transformations:**
- Adopts Java 21 features (Virtual Threads, Pattern Matching, etc.)
- Updates to latest API patterns
- Removes deprecated API usage
- Optimizes for performance improvements

**Key Sub-recipes:**

```yaml
# Core Java 21 migration
- org.openrewrite.java.migrate.UpgradeToJava21

# Pattern matching enhancements
- org.openrewrite.java.migrate.ReplaceInstanceOfPatternMatching

# Switch expressions
- org.openrewrite.java.migrate.SwitchExpressionMigration

# Records
- org.openrewrite.java.migrate.DataClassToRecord
```

**Optional Modern Features:**

```yaml
# Migrate to virtual threads
- org.openrewrite.java.migrate.concurrent.JavaConcurrentAPIs

# Use enhanced switch
- org.openrewrite.java.migrate.SwitchToEnhancedSwitch

# Text blocks
- org.openrewrite.java.migrate.StringConcatToTextBlock
```

---

## Framework-Specific Recipes

### Spring Boot Upgrades

**Spring Boot 2.x → 3.x:**

```yaml
# Complete Spring Boot 3 upgrade
- org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0
- org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_1
- org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2

# Specific migrations
- org.openrewrite.java.spring.boot3.SpringBatch4To5Migration
- org.openrewrite.java.spring.boot3.SpringBootProperties_3_0
- org.openrewrite.java.spring.boot3.ConfigurationOverEnableSecurity
```

**Spring Framework 5 → 6:**

```yaml
- org.openrewrite.java.spring.framework.UpgradeSpringFramework_6_0
```

**Configuration Example:**

```groovy
rewrite {
    activeRecipe(
        'org.openrewrite.java.migrate.Java17',
        'org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2'
    )
}

dependencies {
    rewrite('org.openrewrite.recipe:rewrite-spring:5.0.0')
}
```

### Hibernate / JPA Upgrades

**Hibernate 5.x → 6.x:**

```yaml
- org.openrewrite.java.jpa.UpgradeToJPA2_2
- org.openrewrite.hibernate.MigrateToHibernate60
- org.openrewrite.hibernate.MigrateToHibernate61
```

### JUnit 4 → JUnit 5

**Complete migration:**

```yaml
- org.openrewrite.java.testing.junit5.JUnit5BestPractices
- org.openrewrite.java.testing.junit5.JUnit4to5Migration
```

**What it transforms:**

```java
// Before (JUnit 4)
import org.junit.Test;
import org.junit.Assert;

public class MyTest {
    @Test
    public void testSomething() {
        Assert.assertEquals(1, 1);
    }
}

// After (JUnit 5)
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Assertions;

class MyTest {
    @Test
    void testSomething() {
        Assertions.assertEquals(1, 1);
    }
}
```

### Mockito Upgrades

```yaml
# Mockito 3.x → 4.x (for Java 11+)
- org.openrewrite.java.testing.mockito.Mockito1to4Migration
```

---

## Security and Dependency Recipes

### CVE Vulnerability Fixes

**Scan and fix vulnerabilities:**

```yaml
# Check for vulnerable dependencies
- org.openrewrite.java.dependencies.DependencyVulnerabilityCheck

# Upgrade to fix CVEs
- org.openrewrite.java.dependencies.UpgradeDependencyVersion:
    groupId: com.fasterxml.jackson.core
    artifactId: jackson-databind
    newVersion: 2.15.x
```

### Security Best Practices

```yaml
# Secure random number generation
- org.openrewrite.java.security.SecureRandomPrefersDefaultSeed

# File handling security
- org.openrewrite.java.security.UseFilesCreateTempDirectory

# XML security
- org.openrewrite.java.security.XmlParserXXEVulnerability

# SQL injection prevention
- org.openrewrite.java.security.SecureTempFileCreation
```

### Dependency Updates

**Upgrade specific dependency:**

```yaml
- org.openrewrite.java.dependencies.UpgradeDependencyVersion:
    groupId: org.springframework.boot
    artifactId: spring-boot-starter-parent
    newVersion: 3.2.x
```

**Find and upgrade outdated dependencies:**

```yaml
- org.openrewrite.maven.UpgradePluginVersion:
    groupId: org.apache.maven.plugins
    artifactId: maven-compiler-plugin
    newVersion: 3.11.0
```

---

## Custom Recipe Development

### Simple Recipe (Visitor Pattern)

Create custom recipes for project-specific transformations:

```java
package com.example.recipes;

import org.openrewrite.*;
import org.openrewrite.java.*;

public class RenameMethodRecipe extends Recipe {
    
    @Override
    public String getDisplayName() {
        return "Rename deprecated method";
    }
    
    @Override
    public String getDescription() {
        return "Renames oldMethod() to newMethod()";
    }
    
    @Override
    public TreeVisitor<?, ExecutionContext> getVisitor() {
        return new JavaIsoVisitor<ExecutionContext>() {
            @Override
            public J.MethodInvocation visitMethodInvocation(
                J.MethodInvocation method, 
                ExecutionContext ctx
            ) {
                J.MethodInvocation m = super.visitMethodInvocation(method, ctx);
                if (m.getName().getSimpleName().equals("oldMethod")) {
                    m = m.withName(m.getName().withSimpleName("newMethod"));
                }
                return m;
            }
        };
    }
}
```

### Recipe Configuration (YAML)

Define recipes with parameters:

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.example.UpdateDependencies
displayName: Update Project Dependencies
recipeList:
  - org.openrewrite.java.dependencies.UpgradeDependencyVersion:
      groupId: org.springframework.boot
      artifactId: spring-boot-starter-web
      newVersion: 3.2.0
  - org.openrewrite.java.dependencies.UpgradeDependencyVersion:
      groupId: org.hibernate.orm
      artifactId: hibernate-core
      newVersion: 6.2.0
```

### Testing Custom Recipes

```java
@Test
void testRenameMethod() {
    rewriteRun(
        spec -> spec.recipe(new RenameMethodRecipe()),
        java(
            """
            class Test {
                void example() {
                    oldMethod();
                }
            }
            """,
            """
            class Test {
                void example() {
                    newMethod();
                }
            }
            """
        )
    );
}
```

---

## Recipe Best Practices

### 1. Compose Recipes Strategically

Order matters - run recipes in logical sequence:

```yaml
recipeList:
  # 1. Update Java version first
  - org.openrewrite.java.migrate.Java21
  
  # 2. Migrate packages
  - org.openrewrite.java.migrate.JavaxToJakarta
  
  # 3. Update frameworks
  - org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2
  
  # 4. Fix security issues
  - org.openrewrite.java.security.SecureRandomPrefersDefaultSeed
  
  # 5. Clean up code
  - org.openrewrite.java.cleanup.Cleanup
  
  # 6. Format
  - org.openrewrite.java.format.AutoFormat
```

### 2. Use Dry Run First

Always preview changes:

```bash
mvn rewrite:dryRun
# Review the diff
git diff
```

### 3. Run Incrementally

For large codebases, apply recipes incrementally:

```bash
# Run one recipe at a time
mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.java.migrate.Java17
git commit -m "Apply Java 17 migration recipe"

mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.java.migrate.JavaxToJakarta
git commit -m "Migrate javax to jakarta packages"
```

### 4. Validate After Each Recipe

```bash
mvn clean verify
```

Ensure the code still compiles and tests pass.

### 5. Export Data Tables

Track recipe metrics:

```groovy
rewrite {
    exportDatatables = true
}
```

Generates reports on what changed and why.

---

## Common Recipe Combinations

### Java 11 → 17 with Spring Boot 2 → 3

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.example.Java17SpringBoot3Upgrade
displayName: Java 17 + Spring Boot 3 Upgrade
recipeList:
  - org.openrewrite.java.migrate.Java17
  - org.openrewrite.java.migrate.JavaxToJakarta
  - org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0
  - org.openrewrite.java.spring.boot3.SpringBootProperties_3_0
  - org.openrewrite.java.testing.junit5.JUnit4to5Migration
  - org.openrewrite.java.cleanup.Cleanup
```

### Java 17 → 21 with Security Hardening

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.example.Java21WithSecurity
displayName: Java 21 + Security Fixes
recipeList:
  - org.openrewrite.java.migrate.Java21
  - org.openrewrite.java.dependencies.DependencyVulnerabilityCheck
  - org.openrewrite.java.security.SecureRandomPrefersDefaultSeed
  - org.openrewrite.java.security.UseFilesCreateTempDirectory
  - org.openrewrite.java.security.XmlParserXXEVulnerability
  - org.openrewrite.java.cleanup.Cleanup
```

### Modernization Recipe (Records, Pattern Matching, Switch Expressions)

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.example.ModernJava
displayName: Modern Java Features Adoption
recipeList:
  - org.openrewrite.java.migrate.DataClassToRecord
  - org.openrewrite.java.migrate.ReplaceInstanceOfPatternMatching
  - org.openrewrite.java.migrate.SwitchToEnhancedSwitch
  - org.openrewrite.java.migrate.StringConcatToTextBlock
  - org.openrewrite.java.cleanup.Cleanup
```

---

## Troubleshooting

### Recipe Not Found

Ensure the recipe dependency is added:

```xml
<dependency>
    <groupId>org.openrewrite.recipe</groupId>
    <artifactId>rewrite-migrate-java</artifactId>
    <version>2.0.0</version>
</dependency>
```

### No Changes Applied

Check:
1. Recipe is active in configuration
2. Source files match recipe criteria
3. Java version in pom.xml/build.gradle is correct

### Build Failures After Recipe

1. Review the diff - may need manual fixes
2. Check if imports were updated correctly
3. Verify dependency versions are compatible

### Performance Issues

For large codebases:
- Increase JVM heap: `MAVEN_OPTS="-Xmx4g"`
- Run recipes on submodules separately
- Use parallel builds if supported

---

## Resources

- **Official Docs:** https://docs.openrewrite.org/
- **Recipe Catalog:** https://docs.openrewrite.org/recipes
- **GitHub:** https://github.com/openrewrite
- **Slack Community:** https://join.slack.com/t/rewriteoss/shared_invite/
