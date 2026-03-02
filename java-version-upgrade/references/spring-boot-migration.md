# Spring Boot Migration Reference

Comprehensive guide for upgrading Spring Boot alongside Java version upgrades. Spring Boot is the most widely used Java framework and its version is tightly coupled to Java version requirements.

Source: [Spring Boot 3.0 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide)

---

## Table of Contents

- [Spring Boot and Java Version Compatibility](#spring-boot-and-java-version-compatibility)
- [Pre-Upgrade Checklist](#pre-upgrade-checklist)
- [Spring Boot 2.x to 3.0 Migration](#spring-boot-2x-to-30-migration)
  - [Jakarta EE Migration](#jakarta-ee-migration)
  - [Configuration Properties Migration](#configuration-properties-migration)
  - [Spring Security Changes](#spring-security-changes)
  - [Web Application Changes](#web-application-changes)
  - [Data Access Changes](#data-access-changes)
  - [Actuator Changes](#actuator-changes)
  - [Micrometer and Metrics Changes](#micrometer-and-metrics-changes)
  - [Spring Batch Changes](#spring-batch-changes)
  - [Spring Session Changes](#spring-session-changes)
  - [Build Tool Changes](#build-tool-changes)
  - [Dependency Coordinate Changes](#dependency-coordinate-changes)
- [Spring Boot 3.1 and 3.2 Enhancements](#spring-boot-31-and-32-enhancements)
- [Spring Boot 3.x to 4.0 (Upcoming)](#spring-boot-3x-to-40-upcoming)
- [OpenRewrite Recipes for Spring Boot](#openrewrite-recipes-for-spring-boot)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Spring Boot and Java Version Compatibility

| Spring Boot Version | Min Java | Max Java | Spring Framework | Jakarta EE | Status |
| ------------------- | -------- | -------- | ---------------- | ---------- | ------ |
| 2.7.x | 8 | 21* | 5.3.x | Java EE 8 (javax) | Maintenance (EOL Nov 2023) |
| 3.0.x | 17 | 21 | 6.0.x | Jakarta EE 10 (jakarta) | EOL Nov 2023 |
| 3.1.x | 17 | 21 | 6.0.x | Jakarta EE 10 | EOL May 2024 |
| 3.2.x | 17 | 22 | 6.1.x | Jakarta EE 10 | EOL Nov 2024 |
| 3.3.x | 17 | 23 | 6.1.x | Jakarta EE 10 | Current |
| 3.4.x | 17 | 24 | 6.2.x | Jakarta EE 10 | Current |
| 4.0.x (planned) | 17+ | 25+ | 7.0.x | Jakarta EE 11 | Planned |

*Spring Boot 2.7.x has limited Java 21 support — some features may not work fully.

**Key Rule:** Spring Boot 3.x requires Java 17 or later. If upgrading from Java 8 or 11, you must also upgrade Spring Boot from 2.x to 3.x.

---

## Pre-Upgrade Checklist

### 1. Upgrade to Latest Spring Boot 2.7.x First

Before jumping to 3.0, upgrade to the latest 2.7.x release:

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.7.18</version>
</parent>
```

This ensures you're building against the most recent compatible dependencies and makes the 3.0 migration smoother.

### 2. Review Spring Security 5.8 Bridge

Spring Boot 3.0 uses Spring Security 6.0. The Spring Security team provides a stepping-stone release:

```
Spring Security 5.x → 5.8 (bridge) → 6.0
```

Upgrade your Spring Boot 2.7 app to Spring Security 5.8 first to simplify the migration:

- [Spring Security 5.8 Migration Guide](https://docs.enterprise.spring.io/spring-security/reference/5.8/migration/index.html)
- [Spring Security 5.8 to 6.0 Migration Guide](https://docs.enterprise.spring.io/spring-security/reference/6.0/migration/index.html)

### 3. Review Deprecations

Classes, methods, and properties deprecated in Spring Boot 2.x have been **removed** in 3.0. Fix all deprecation warnings before upgrading.

### 4. Identify Non-Managed Dependencies

Dependencies not managed by Spring Boot (e.g., Spring Cloud, third-party libraries) need their compatible versions identified separately.

---

## Spring Boot 2.x to 3.0 Migration

### Jakarta EE Migration

**This is the single biggest change in Spring Boot 3.0.**

Spring Boot 3.0 upgraded from Java EE (javax) to Jakarta EE 10 (jakarta). All `javax.*` packages that are part of Jakarta EE have been renamed to `jakarta.*`.

**Package renames:**

```java
// BEFORE (Spring Boot 2.x)
import javax.servlet.http.HttpServletRequest;
import javax.persistence.Entity;
import javax.persistence.Column;
import javax.validation.constraints.NotNull;
import javax.annotation.PostConstruct;
import javax.transaction.Transactional;

// AFTER (Spring Boot 3.x)
import jakarta.servlet.http.HttpServletRequest;
import jakarta.persistence.Entity;
import jakarta.persistence.Column;
import jakarta.validation.constraints.NotNull;
import jakarta.annotation.PostConstruct;
import jakarta.transaction.Transactional;
```

**Common javax → jakarta package mappings:**

| javax Package | jakarta Package | Affected APIs |
| ------------- | --------------- | ------------- |
| `javax.servlet.*` | `jakarta.servlet.*` | Servlet, Filter, HttpSession |
| `javax.persistence.*` | `jakarta.persistence.*` | JPA entities, repositories |
| `javax.validation.*` | `jakarta.validation.*` | Bean Validation |
| `javax.annotation.*` | `jakarta.annotation.*` | @PostConstruct, @PreDestroy |
| `javax.transaction.*` | `jakarta.transaction.*` | JTA transactions |
| `javax.mail.*` | `jakarta.mail.*` | JavaMail |
| `javax.websocket.*` | `jakarta.websocket.*` | WebSocket |
| `javax.xml.bind.*` | `jakarta.xml.bind.*` | JAXB |
| `javax.inject.*` | `jakarta.inject.*` | CDI injection |

**Dependency coordinate changes:**

```xml
<!-- BEFORE -->
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
</dependency>

<!-- AFTER -->
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
</dependency>
```

**Automated migration tools:**

- [OpenRewrite Jakarta Migration Recipes](https://docs.openrewrite.org/recipes/java/migrate/jakarta/javaxmigrationtojakarta)
- [Spring Boot Migrator Project](https://github.com/spring-projects-experimental/spring-boot-migrator)
- [IntelliJ IDEA Jakarta Migration Support](https://blog.jetbrains.com/idea/2021/06/intellij-idea-eap-6/)

### Configuration Properties Migration

Several configuration properties were renamed or removed in 3.0. Use the properties migrator module to detect and temporarily fix them:

**Maven:**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

**Gradle:**

```groovy
runtimeOnly("org.springframework.boot:spring-boot-properties-migrator")
```

At startup, this module:

- Scans your `application.properties` / `application.yml`
- Prints diagnostics about renamed/removed properties
- Temporarily migrates properties at runtime

**Important:** Remove this dependency after completing the migration.

**Key property changes:**

```properties
# Redis (moved under spring.data)
# BEFORE:
spring.redis.host=localhost
# AFTER:
spring.data.redis.host=localhost

# Cassandra (moved out of spring.data)
# BEFORE:
spring.data.cassandra.contact-points=localhost
# AFTER:
spring.cassandra.contact-points=localhost

# Actuator metrics export (restructured)
# BEFORE:
management.metrics.export.prometheus.enabled=true
# AFTER:
management.prometheus.metrics.export.enabled=true
```

### Spring Security Changes

Spring Boot 3.0 uses Spring Security 6.0 with significant changes:

**Dispatch type authorization:**

In Servlet applications, Spring Security 6.0 applies authorization to **every dispatch type** (not just REQUEST). Configure using:

```properties
spring.security.filter.dispatcher-types=request,error,async
```

**SAML2 property rename:**

```properties
# BEFORE:
spring.security.saml2.relyingparty.registration.{id}.identity-provider.*
# AFTER:
spring.security.saml2.relyingparty.registration.{id}.asserting-party.*
```

**ReactiveUserDetailsService:**

No longer auto-configured when an `AuthenticationManagerResolver` is present. Define your own `ReactiveUserDetailsService` bean if needed.

### Web Application Changes

**Trailing slash matching disabled:**

Spring Framework 6.0 sets `useTrailingSlashMatch` to `false` by default. `/some/path/` no longer matches `/some/path`.

```java
// Temporary workaround — configure explicitly
@Configuration
public class WebConfiguration implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUseTrailingSlashMatch(true);
    }
}
```

**Better approach:** Update URLs or add explicit route mappings.

**HTTP header size property:**

```properties
# BEFORE (deprecated):
server.max-http-header-size=8KB
# AFTER:
server.max-http-request-header-size=8KB
```

**Auto-configuration file format:**

```
# REMOVED in 3.0:
META-INF/spring.factories (for auto-configuration registration)

# REQUIRED:
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

Libraries targeting both 2.x and 3.x can list auto-configurations in **both** files.

**Apache HttpClient replaced:**

```xml
<!-- BEFORE (removed in Spring Framework 6.0) -->
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
</dependency>

<!-- AFTER -->
<dependency>
    <groupId>org.apache.httpcomponents.client5</groupId>
    <artifactId>httpclient5</artifactId>
</dependency>
```

**Logging date format changed:**

Default log format changed to ISO-8601: `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`

To restore old format:

```properties
logging.pattern.dateformat=yyyy-MM-dd HH:mm:ss.SSS
```

**@ConstructorBinding no longer needed at type level:**

```java
// BEFORE (Spring Boot 2.x)
@ConstructorBinding
@ConfigurationProperties("my.config")
public class MyConfig {
    // ...
}

// AFTER (Spring Boot 3.x) — remove @ConstructorBinding from class level
@ConfigurationProperties("my.config")
public class MyConfig {
    // Only needed when multiple constructors exist
}
```

**Graceful shutdown phases updated:**

- Graceful shutdown begins in phase `SmartLifecycle.DEFAULT_PHASE - 2048`
- Web server stops in phase `SmartLifecycle.DEFAULT_PHASE - 1024`

### Data Access Changes

**Hibernate 6.1:**

Spring Boot 3.0 uses Hibernate 6.1 (up from 5.x):

- Group ID changed: `org.hibernate` → `org.hibernate.orm`
- `spring.jpa.hibernate.use-new-id-generator-mappings` removed
- Review [Hibernate 6.0](https://docs.jboss.org/hibernate/orm/6.0/migration-guide/migration-guide.html) and [6.1](https://docs.jboss.org/hibernate/orm/6.1/migration-guide/migration-guide.html) migration guides

**Flyway 9.0:**

Updated to Flyway 9.0. `FlywayConfigurationCustomizer` beans are now called **after** `Callback` and `JavaMigration` beans are added.

**Liquibase 4.17.x:**

Some users have reported issues with 4.17.x. Override the version if affected:

```xml
<properties>
    <liquibase.version>4.20.0</liquibase.version>
</properties>
```

**Embedded MongoDB removed:**

Auto-configuration for Flapdoodle embedded MongoDB removed. Use:

- [Flapdoodle Spring auto-configuration](https://github.com/flapdoodle-oss/de.flapdoodle.embed.mongo.spring)
- [Testcontainers](https://www.testcontainers.org/) (recommended)

**Elasticsearch client migration:**

High-level REST client removed. Use the new Java client:

```xml
<!-- BEFORE (removed) -->
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-high-level-client</artifactId>
</dependency>

<!-- AFTER -->
<dependency>
    <groupId>co.elastic.clients</groupId>
    <artifactId>elasticsearch-java</artifactId>
</dependency>
```

**MySQL JDBC driver coordinates changed:**

```xml
<!-- BEFORE -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
</dependency>

<!-- AFTER -->
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency>
```

**R2DBC 1.0:**

`r2dbc-bom.version` no longer available. Use individual module version properties:

- `oracle-r2dbc.version`
- `r2dbc-h2.version`
- `r2dbc-pool.version`
- `r2dbc-postgres.version`

### Actuator Changes

**Default JMX exposure restricted:**

Only the `health` endpoint is exposed over JMX by default. Configure with:

```properties
management.endpoints.jmx.exposure.include=health,info,metrics
```

**httptrace renamed to httpexchanges:**

```java
// BEFORE
HttpTraceRepository

// AFTER
HttpExchangeRepository
// Package: org.springframework.boot.actuate.web.exchanges
```

**Actuator JSON uses isolated ObjectMapper:**

To revert to application ObjectMapper:

```properties
management.endpoints.jackson.isolated-object-mapper=false
```

**Endpoint sanitization stricter:**

`/env` and `/configprops` mask all values by default:

```properties
# Options: NEVER (default), ALWAYS, WHEN_AUTHORIZED
management.endpoint.env.show-values=WHEN_AUTHORIZED
management.endpoint.configprops.show-values=WHEN_AUTHORIZED
```

### Micrometer and Metrics Changes

Spring Boot 3.0 uses Micrometer 1.10 with Observation API integration:

**Key changes:**

- `WebMvcMetricsFilter` removed → replaced by `ServerHttpObservationFilter`
- `MetricsRestTemplateCustomizer` removed → replaced by `ObservationRestTemplateCustomizer`
- `*TagProvider` and `*TagContributor` deprecated → replaced by `ObservationConvention`
- `JvmInfoMetrics` auto-configured (remove manual bean definitions)

**Migrating custom tag providers:**

```java
// BEFORE (Spring Boot 2.x) — TagContributor/TagProvider
public class CustomTagProvider implements WebMvcTagsProvider {
    // ...
}

// AFTER (Spring Boot 3.x) — ObservationConvention
public class CustomObservationConvention
        extends DefaultServerRequestObservationConvention {

    @Override
    public KeyValues getLowCardinalityKeyValues(
            ServerRequestObservationContext context) {
        return super.getLowCardinalityKeyValues(context)
                .and(KeyValue.of("custom.key", "value"));
    }
}
```

**Metrics export properties restructured:**

```properties
# BEFORE:
management.metrics.export.prometheus.enabled=true
management.metrics.export.datadog.api-key=xxx

# AFTER:
management.prometheus.metrics.export.enabled=true
management.datadog.metrics.export.api-key=xxx
```

### Spring Batch Changes

Spring Boot 3.0 uses Spring Batch 5.0:

**@EnableBatchProcessing discouraged:**

```java
// BEFORE (Spring Boot 2.x) — required
@EnableBatchProcessing
@SpringBootApplication
public class BatchApp { }

// AFTER (Spring Boot 3.x) — remove it; auto-configuration handles it
@SpringBootApplication
public class BatchApp { }
```

**Multiple batch jobs:**

Running multiple batch jobs is no longer supported by default. Specify the job to run:

```properties
spring.batch.job.name=myJob
```

### Spring Session Changes

**Store type auto-detection:**

`spring.session.store-type` is no longer supported. Spring Boot uses a fixed order to determine which `SessionRepository` to auto-configure when multiple implementations are on the classpath.

### Build Tool Changes

**Maven:**

- `fork` attribute removed from `spring-boot:run` and `spring-boot:start`
- Git Commit ID Plugin coordinates changed:

```xml
<!-- BEFORE -->
<groupId>pl.project13.maven</groupId>
<artifactId>git-commit-id-plugin</artifactId>

<!-- AFTER -->
<groupId>io.github.git-commit-id</groupId>
<artifactId>git-commit-id-maven-plugin</artifactId>
```

**Gradle:**

- Main class resolution simplified — looks only in main source set output
- Task properties now use Gradle `Property` API (use `.get()`, `.set()`)
- Build info exclusions use name-based mechanism:

```groovy
springBoot {
    buildInfo {
        excludes = ['time']
    }
}
```

### Dependency Coordinate Changes

| Before | After | Notes |
| ------ | ----- | ----- |
| `mysql:mysql-connector-java` | `com.mysql:mysql-connector-j` | GroupId changed |
| `org.hibernate:hibernate-core` | `org.hibernate.orm:hibernate-core` | GroupId changed |
| `pl.project13.maven:git-commit-id-plugin` | `io.github.git-commit-id:git-commit-id-maven-plugin` | Complete change |
| `org.apache.httpcomponents:httpclient` | `org.apache.httpcomponents.client5:httpclient5` | Major version |
| `org.elasticsearch.client:elasticsearch-rest-high-level-client` | `co.elastic.clients:elasticsearch-java` | New client |
| Apache Johnzon (JSON-B) | Eclipse Yasson | Default provider changed |
| `antlr:antlr` (ANTLR 2) | — | Management removed |
| RxJava 1.x/2.x | RxJava 3 | Only 3 managed |
| Ehcache (no classifier) | Ehcache (`jakarta` classifier) | Classifier required |

**Removed support (no longer managed):**

- Apache ActiveMQ (classic) — use Artemis
- Atomikos — use alternative JTA provider
- EhCache 2 — use EhCache 3
- Hazelcast 3 — use Hazelcast 5+
- Apache Solr (Jetty incompatibility)

---

## Spring Boot 3.1 and 3.2 Enhancements

After migrating to 3.0, consider upgrading to the latest 3.x for additional improvements:

### Spring Boot 3.1

- Docker Compose support (`spring-boot-docker-compose` module)
- Testcontainers at development time
- SSL bundle configuration
- Improved native image support

### Spring Boot 3.2

- Virtual thread support (Java 21)
- RestClient (new synchronous HTTP client)
- JdbcClient (new simple JDBC interface)
- Improved observability with Micrometer 1.12
- CRaC (Coordinated Restore at Checkpoint) support

**Virtual threads in Spring Boot 3.2:**

```properties
# Enable virtual threads (requires Java 21)
spring.threads.virtual.enabled=true
```

This enables virtual threads for:

- Tomcat request handling
- Spring MVC @Async methods
- @Scheduled methods
- Spring WebFlux blocking calls

---

## Spring Boot 3.x to 4.0 (Upcoming)

Spring Boot 4.0 is planned with:

- Spring Framework 7.0
- Jakarta EE 11 support
- Java 17+ (minimum)
- Removal of APIs deprecated in 3.x

**Preparation:** Fix all deprecation warnings in your Spring Boot 3.x application now.

---

## OpenRewrite Recipes for Spring Boot

### Complete Spring Boot 3.0 Upgrade

```yaml
type: specs.openrewrite.org/v1beta/recipe
name: com.example.SpringBoot3FullUpgrade
displayName: Complete Spring Boot 2.x to 3.x Upgrade
recipeList:
  # Step 1: Java 17 migration
  - org.openrewrite.java.migrate.Java17

  # Step 2: Jakarta EE migration
  - org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta

  # Step 3: Spring Boot 3.0 upgrade
  - org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0

  # Step 4: Spring Boot configuration properties
  - org.openrewrite.java.spring.boot3.SpringBootProperties_3_0

  # Step 5: Spring Security migration
  - org.openrewrite.java.spring.security6.UpgradeSpringSecurity_6_0

  # Step 6: Spring Batch migration
  - org.openrewrite.java.spring.boot3.SpringBatch4To5Migration

  # Step 7: Continue to latest 3.x
  - org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_1
  - org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_2
  - org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_3

  # Step 8: Testing migration
  - org.openrewrite.java.testing.junit5.JUnit4to5Migration
  - org.openrewrite.java.testing.mockito.Mockito4to5Migration
```

### Maven Configuration

```xml
<plugin>
    <groupId>org.openrewrite.maven</groupId>
    <artifactId>rewrite-maven-plugin</artifactId>
    <version>5.20.0</version>
    <configuration>
        <activeRecipes>
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

### Gradle Configuration

```groovy
plugins {
    id 'org.openrewrite.rewrite' version '6.1.0'
}

rewrite {
    activeRecipe(
        'org.openrewrite.java.spring.boot3.UpgradeSpringBoot_3_0'
    )
}

dependencies {
    rewrite('org.openrewrite.recipe:rewrite-spring:5.0.0')
    rewrite('org.openrewrite.recipe:rewrite-migrate-java:2.0.0')
}
```

---

## Troubleshooting Common Issues

### javax imports still present after migration

```bash
# Find remaining javax imports
grep -rn "import javax\." --include="*.java" src/

# Note: javax.crypto.*, javax.net.*, javax.security.auth.*,
# javax.security.cert.* are part of the JDK and do NOT change to jakarta
```

**JDK javax packages that do NOT migrate:**

- `javax.crypto.*`
- `javax.net.*`
- `javax.security.auth.*`
- `javax.security.cert.*`
- `javax.sql.*` (in java.sql module)
- `javax.xml.crypto.*`
- `javax.xml.transform.*`
- `javax.xml.parsers.*`

### ClassNotFoundException for javax classes

Typically caused by a transitive dependency still using old coordinates. Check:

```bash
# Maven
mvn dependency:tree | grep javax

# Gradle
./gradlew dependencies | grep javax
```

### Spring Security filter chain errors

Spring Security 6.0 changes the default behavior. Common fix:

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .anyRequest().authenticated()
        )
        .httpBasic(Customizer.withDefaults());
    return http.build();
}
```

Note: Lambda DSL is now required — the old chain-style `.and()` method approach is removed.

### Embedded server fails to start (Jetty)

Jetty doesn't support Servlet 6.0 in all versions. Downgrade the Servlet API:

```properties
jakarta-servlet.version=5.0.0
```

Or switch to Tomcat (default) or Undertow.

### Hibernate ID generation changes

Hibernate 6.x changes default ID generation strategy. If you see unexpected ID values:

```properties
# Check Hibernate migration guides
# May need to add @GeneratedValue strategy explicitly
```

### Properties not being read

Use the properties migrator to diagnose:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

Check startup logs for migration warnings and apply the suggested property renames.
