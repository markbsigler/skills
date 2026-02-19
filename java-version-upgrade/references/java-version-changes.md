# Java Version-Specific Changes Reference

Comprehensive guide to breaking changes, new features, and deprecations across Java versions.

## Table of Contents

- [Java 8 → 11](#java-8--11)
- [Java 11 → 17](#java-11--17)
- [Java 17 → 21](#java-17--21)
- [Oracle Official Removed APIs by Version](#oracle-official-removed-apis-by-version)
- [Preparing for Migration (Oracle Guidelines)](#preparing-for-migration-oracle-guidelines)
- [Common Migration Patterns](#common-migration-patterns)

---

## Java 8 → 11

### Breaking Changes

#### Removed Modules (JEP 320)

Java 11 removed several Java EE and CORBA modules:

- **javax.xml.bind (JAXB)** - XML binding
- **javax.activation (JAF)** - JavaBeans Activation Framework
- **javax.xml.ws (JAX-WS)** - Web services
- **javax.annotation** - Common annotations
- **java.corba** - CORBA support
- **java.transaction** - JTA

**Migration:**
```xml
<!-- Add as explicit dependencies -->
<dependency>
    <groupId>javax.xml.bind</groupId>
    <artifactId>jaxb-api</artifactId>
    <version>2.3.1</version>
</dependency>
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>2.3.1</version>
</dependency>
<dependency>
    <groupId>javax.annotation</groupId>
    <artifactId>javax.annotation-api</artifactId>
    <version>1.3.2</version>
</dependency>
```

#### Removed Tools

- **Java Applet API** - Deprecated in 9, removed in 11
- **JavaFX** - Unbundled, now separate OpenJFX project
- **Nashorn JavaScript Engine** - Deprecated in 11, removed in 15

#### Classloader Changes

- `ClassLoader.getSystemClassLoader()` no longer returns URLClassLoader
- Can affect reflection-based frameworks

### New Features

#### Local-Variable Type Inference (var) - Java 10

```java
var list = new ArrayList<String>();
var stream = list.stream();
```

#### HTTP Client API - Java 11 (JEP 321)

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com"))
    .build();
HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());
```

#### String Methods - Java 11

```java
"  ".isBlank()           // true
"Hello".repeat(3)        // "HelloHelloHello"
"A\nB\nC".lines()        // Stream of lines
" text ".strip()         // "text" (Unicode-aware)
```

#### Collection Factory Methods - Java 9

```java
List<String> list = List.of("a", "b", "c");
Set<String> set = Set.of("a", "b", "c");
Map<String, Integer> map = Map.of("a", 1, "b", 2);
```

### Performance Improvements

- **G1GC** - Default garbage collector (Java 9+)
- **Compact Strings** - Reduced memory for Latin-1 strings
- **Application Class-Data Sharing** - Faster startup

---

## Java 11 → 17

### Breaking Changes

#### Strong Encapsulation of JDK Internals (JEP 403)

Java 17 strongly encapsulates internal APIs. Code using `sun.*` packages will fail.

**Common Issues:**
```java
// These will fail in Java 17:
sun.misc.Unsafe
sun.reflect.ReflectionFactory
com.sun.org.apache.xerces.*
```

**Solutions:**
1. Migrate to public APIs
2. Use `--add-opens` for legacy code (temporary):
   ```bash
   --add-opens java.base/java.lang=ALL-UNNAMED
   --add-opens java.base/java.util=ALL-UNNAMED
   ```

#### Removed APIs

- **Nashorn Engine** - Completely removed (use GraalVM or other JS engines)
- **RMI Activation** - Removed (JEP 407)
- **Experimental AOT/JIT** - Removed

#### Security Manager Deprecation (JEP 411)

SecurityManager deprecated for removal. Prepare alternatives if using.

### New Features

#### Records (JEP 395) - Java 16

Immutable data classes:

```java
public record Person(String name, int age) {
    // Compact constructor
    public Person {
        if (age < 0) throw new IllegalArgumentException();
    }
    
    // Additional methods allowed
    public String greeting() {
        return "Hello, " + name;
    }
}
```

#### Pattern Matching for instanceof (JEP 394) - Java 16

```java
// Before
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.toUpperCase());
}

// After
if (obj instanceof String s) {
    System.out.println(s.toUpperCase());
}
```

#### Sealed Classes (JEP 409) - Java 17

Control inheritance hierarchy:

```java
public sealed interface Shape
    permits Circle, Rectangle, Triangle {
}

public final class Circle implements Shape { }
public final class Rectangle implements Shape { }
public non-sealed class Triangle implements Shape { }
```

#### Switch Expressions (JEP 361) - Java 14

```java
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY -> 7;
    case THURSDAY, SATURDAY -> 8;
    case WEDNESDAY -> 9;
    default -> throw new IllegalStateException();
};
```

#### Text Blocks (JEP 378) - Java 15

```java
String html = """
    <html>
        <body>
            <p>Hello, World!</p>
        </body>
    </html>
    """;

String query = """
    SELECT id, name, email
    FROM users
    WHERE status = 'active'
    ORDER BY name
    """;
```

#### Helpful NullPointerExceptions (JEP 358) - Java 14

More informative NPE messages:
```
Cannot invoke "String.length()" because "name" is null
```

### Performance Improvements

- **ZGC** - Production-ready low-latency GC (JEP 377)
- **Shenandoah GC** - Low-pause-time GC
- **Enhanced Pseudo-Random Number Generators** (JEP 356)

---

## Java 17 → 21

### Breaking Changes

#### Stricter Thread Safety

Some internal implementations became stricter about concurrent access.

#### Finalized Removals

- Continued removal of deprecated APIs from earlier versions

### New Features

#### Virtual Threads (JEP 444) - Java 21

Lightweight threads for high-throughput concurrent applications:

```java
// Create and start virtual thread
Thread.startVirtualThread(() -> {
    System.out.println("Running in virtual thread");
});

// Using ExecutorService
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            // Handle request
            return processRequest(i);
        });
    });
}

// Structured concurrency (preview)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<Integer> order = scope.fork(() -> fetchOrder());
    
    scope.join();
    scope.throwIfFailed();
    
    return new Response(user.resultNow(), order.resultNow());
}
```

#### Pattern Matching for switch (JEP 441) - Java 21

```java
// Type patterns
String formatted = switch (obj) {
    case Integer i -> String.format("int %d", i);
    case Long l    -> String.format("long %d", l);
    case Double d  -> String.format("double %f", d);
    case String s  -> String.format("String %s", s);
    default        -> obj.toString();
};

// Guarded patterns
String result = switch (obj) {
    case String s when s.length() > 5 -> "Long string: " + s;
    case String s -> "Short string: " + s;
    case Integer i when i > 0 -> "Positive: " + i;
    case Integer i -> "Non-positive: " + i;
    default -> "Unknown";
};

// Record patterns
record Point(int x, int y) {}

static void printPoint(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        System.out.println("x: " + x + ", y: " + y);
    }
}
```

#### Record Patterns (JEP 440) - Java 21

Deconstruct records in pattern matching:

```java
record Point(int x, int y) {}
record Circle(Point center, int radius) {}

static void printCircle(Object obj) {
    if (obj instanceof Circle(Point(var x, var y), var r)) {
        System.out.println("Circle at (" + x + "," + y + 
                         ") with radius " + r);
    }
}
```

#### Sequenced Collections (JEP 431) - Java 21

New interfaces for collections with defined encounter order:

```java
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();
    void addFirst(E);
    void addLast(E);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}

List<String> list = new ArrayList<>();
list.addFirst("first");
list.addLast("last");
String first = list.getFirst();
List<String> reversed = list.reversed();
```

#### String Templates (Preview JEP 430) - Java 21

```java
// Preview feature - enable with --enable-preview
String name = "Joan";
String info = STR."My name is \{name}";

int x = 10, y = 20;
String result = STR."\{x} + \{y} = \{x + y}";
```

#### Unnamed Patterns and Variables (Preview JEP 443) - Java 21

```java
// Use _ for unused variables
switch (obj) {
    case Point(int x, _) -> x;  // y coordinate unused
    case Circle(_, int r) -> r;  // center unused
}

// In catch blocks
try {
    // ...
} catch (Exception _) {
    // Exception unused
}
```

### Performance Improvements

- **Generational ZGC** (JEP 439) - Improved ZGC performance
- **Vector API Enhancements** - SIMD operations
- **Foreign Function & Memory API** - Native interop performance

---

## Common Migration Patterns

### Pattern 1: Replacing Removed JAXB

**Before (Java 8):**
```java
JAXBContext context = JAXBContext.newInstance(MyClass.class);
Marshaller marshaller = context.createMarshaller();
```

**After (Java 11+):**
```xml
<!-- Add dependency -->
<dependency>
    <groupId>org.glassfish.jaxb</groupId>
    <artifactId>jaxb-runtime</artifactId>
    <version>2.3.1</version>
</dependency>
```

### Pattern 2: Module System Migration

**Add module-info.java:**
```java
module com.example.myapp {
    requires java.sql;
    requires java.net.http;
    requires transitive java.logging;
    
    exports com.example.api;
    opens com.example.model to com.fasterxml.jackson.databind;
}
```

### Pattern 3: Modernizing Exception Handling

**Before:**
```java
try {
    doSomething();
} catch (IOException e) {
    e.printStackTrace();
}
```

**After:**
```java
try {
    doSomething();
} catch (IOException e) {
    logger.error("Failed to do something", e);
    throw new ServiceException("Operation failed", e);
}
```

### Pattern 4: Stream API Improvements

**Java 9+ additions:**
```java
// takeWhile / dropWhile
Stream.of(1,2,3,4,5,6)
    .takeWhile(n -> n < 4)  // [1,2,3]
    .toList();

// ofNullable
Stream.ofNullable(getNullableValue())
    .forEach(System.out::println);

// iterate with predicate
Stream.iterate(0, n -> n < 10, n -> n + 1)
    .forEach(System.out::println);
```

### Pattern 5: Optional Enhancements

**Java 9+:**
```java
optional.ifPresentOrElse(
    value -> System.out.println(value),
    () -> System.out.println("Empty")
);

optional.or(() -> Optional.of(defaultValue));

optional.stream()
    .map(String::toUpperCase)
    .forEach(System.out::println);
```

### Pattern 6: CompletableFuture Improvements

**Java 9+:**
```java
// Timeout support
CompletableFuture<String> future = fetchData()
    .orTimeout(5, TimeUnit.SECONDS)
    .completeOnTimeout("default", 3, TimeUnit.SECONDS);

// Copy
CompletableFuture<String> copy = future.copy();
```

---

## Version-Specific JVM Flags

### Java 9-11
- `--add-modules` - Add modules to root set
- `--add-opens` - Open packages for reflection
- `--illegal-access=permit` - Allow illegal reflection (removed in 17)

### Java 17+
- `--add-opens` - Required for deep reflection
- `--enable-preview` - Enable preview features
- No `--illegal-access` flag

### Java 21+
- `--enable-preview` - For virtual threads, pattern matching enhancements
- `-XX:+UseZGC -XX:+ZGenerational` - Enable generational ZGC

---

## Oracle Official Removed APIs by Version

Source: [Oracle JDK 21 Migration Guide - Removed APIs](https://docs.oracle.com/en/java/javase/21/migrate/removed-apis.html)

Use `jdeprscan --release <version> -l --for-removal` to get the complete list of APIs marked for removal.

### APIs Removed in Java SE 21

**Classes:**

```text
java.lang.Compiler
javax.management.remote.rmi.RMIIIOPServerImpl
```

**Methods:**

```text
java.lang.ThreadGroup.allowThreadSuspension(boolean)
```

### APIs Removed in Java SE 17

**Packages:**

```text
java.rmi.activation (entire package)
```

**Classes (all in java.rmi.activation):**

```text
Activatable, ActivationDesc, ActivationGroup, ActivationGroup_Stub
ActivationGroupDesc, ActivationGroupID, ActivationID
ActivationInstantiator, ActivationMonitor, ActivationSystem, Activator
```

### APIs Removed in Java SE 16

```text
javax.tools.ToolProvider.<init>()
```

### APIs Removed in Java SE 15

```text
java.management.rmi.RMIConnectorServer.CREDENTIAL_TYPES
java.lang.invoke.ConstantBootstraps.<init>
java.lang.reflect.Modifier.<init>
```

### APIs Removed in Java SE 14

**Packages:**

```text
java.security.acl (entire package)
```

**Interfaces:**

```text
java.security.acl.Acl, AclEntry, Group, Owner, Permission
java.util.jar.Pack200.Packer, Pack200.Unpacker
```

### APIs Removed in Java SE 12

```text
java.io.FileInputStream.finalize()
java.io.FileOutputStream.finalize()
java.util.zip.Deflater.finalize()
java.util.zip.Inflater.finalize()
java.util.zip.ZipFile.finalize()
```

### APIs Removed in JDK 11

```text
javax.security.auth.Policy
java.lang.Runtime.runFinalizersOnExit(boolean)
java.lang.SecurityManager.checkAwtEventQueueAccess()
java.lang.SecurityManager.checkMemberAccess(java.lang.Class,int)
java.lang.SecurityManager.checkSystemClipboardAccess()
java.lang.SecurityManager.checkTopLevelWindow(java.lang.Object)
java.lang.System.runFinalizersOnExit(boolean)
java.lang.Thread.destroy()
java.lang.Thread.stop(java.lang.Throwable)
```

### APIs Removed in JDK 9/10

**JDK Internal APIs:**

- `sun.misc.BASE64Encoder` / `sun.misc.BASE64Decoder` → Use `java.util.Base64`
- `sun.misc.Unsafe` → Use `java.lang.invoke.VarHandle` (JEP 193)
- `sun.reflect.Reflection.getCallerClass(int)` → Use Stack-Walking API (JEP 259)
- `java.awt.peer` / `java.awt.dnd.peer` packages → No longer accessible
- `com.sun.image.codec.jpeg` → Use Java Image I/O API (`javax.imageio`)


### Removed Tools and Components

| Tool/Component | Removed In | Replacement |
| -------------- | ---------- | ----------- |
| `javah` | JDK 10 | `javac -h` |
| JavaDB (Apache Derby) | JDK 9 | Download Apache Derby separately |
| `hprof` agent | JDK 9 | Java Flight Recorder (JFR) |
| `java-rmi.exe`/`java-rmi.cgi` | JDK 9 | Standard RMI |
| IIOP/JMX RMI Connector | JDK 9 | — |
| `jvisualvm` | JDK 9 | Download VisualVM separately |
| Nashorn JS Engine | JDK 15 | GraalVM JS engine |
| Security Manager | Deprecated JDK 17 | Alternative security mechanisms |
| Applet API | JDK 11 | Web technologies |

---

## Preparing for Migration (Oracle Guidelines)

Source: [Oracle JDK 21 Migration Guide - Preparing](https://docs.oracle.com/en/java/javase/21/migrate/preparing-migration.html)

### Oracle's Recommended Migration Steps

**1. Run Before Recompiling:**

Try running your existing application on the target JDK without any code changes first. Most code and libraries work without modification.

```bash
# Run application directly on new JDK
$JAVA_21_HOME/bin/java -jar your-application.jar
```

When running, watch for:

- Warnings about obsolete VM options
- VM startup failures (check for removed GC options)
- Behavioral differences in date/currency formatting (CLDR locale data)
- Default charset differences (UTF-8 in JDK 18+)

**2. Run jdeps for Dependency Analysis:**

```bash
# Identify internal API dependencies
jdeps -jdkinternals your-app.jar

# Full module dependency analysis
jdeps --multi-release 21 -s your-app.jar

# Recursive analysis including transitive dependencies
jdeps -R -jdkinternals your-app.jar
```

**3. Run jdeprscan for Deprecated API Usage:**

```bash
# Find usage of deprecated APIs
jdeprscan --release 21 your-app.jar

# List all APIs scheduled for removal
jdeprscan --release 21 -l --for-removal
```

**4. Update Third-Party Libraries:**

Check the [OpenJDK Quality Outreach](https://wiki.openjdk.java.net/display/quality/Quality+Outreach) wiki for FOSS project compatibility with OpenJDK builds.

**5. Default Charset Change (JDK 18+):**

UTF-8 is the default charset since JDK 18 (JEP 400).

```bash
# Check what charset was previously default
java -XshowSettings:properties -version 2>&1 | grep native.encoding

# Test with UTF-8 on current JDK
java -Dfile.encoding=UTF-8 your-application

# Revert to pre-18 behavior (temporary)
java -Dfile.encoding=COMPAT your-application
```

**6. CLDR Locale Data (JDK 9+):**

CLDR is the default locale data provider since JDK 9. Dates, currencies, and numbers may format differently.

```bash
# Revert to JDK 8 locale behavior (temporary)
java -Djava.locale.providers=COMPAT,CLDR your-application
```

**7. Use --release Flag for Compilation:**

```bash
# Preferred compilation approach
javac --release 21 src/**/*.java

# The --release flag ensures API compatibility with the target version
```

**8. Underscore Identifier Restriction:**

Since JDK 9, `_` (underscore) is a keyword and cannot be used as an identifier:

```java
// This will NOT compile in JDK 9+
static Object _ = new Object();  // Error: '_' is a keyword
```

### Strong Encapsulation Timeline

| JDK Version | Behavior |
| ----------- | -------- |
| JDK 9-15 | Warning on illegal reflective access, `--illegal-access=permit` default |
| JDK 16 | `--illegal-access=deny` default, warnings on CLI relaxation |
| JDK 17+ | Strong encapsulation enforced, `--illegal-access` flag removed |

Use `--add-opens` for specific packages as a workaround:

```bash
java --add-opens java.base/java.lang=ALL-UNNAMED \
     --add-opens java.base/java.util=ALL-UNNAMED \
     -jar your-app.jar
```

**Goal:** Eliminate all `--add-opens` flags by upgrading libraries to module-aware versions.

### Significant JDK 21 Features (from Oracle)

**Finalized features:**

- **Record Patterns** (JEP 440) - Deconstruct records in pattern matching
- **Pattern Matching for switch** (JEP 441) - Type patterns and guarded patterns in switch
- **Virtual Threads** (JEP 444) - Lightweight threads for high-throughput concurrency
- **Sequenced Collections** (JEP 431) - Ordered collection interfaces
- **Key Encapsulation Mechanism API** (JEP 452) - KEM for public key cryptography
- **Generational ZGC** (JEP 439) - Improved Z Garbage Collector performance

**Preview features (JDK 21):**

- String Templates (JEP 430)
- Unnamed Patterns and Variables (JEP 443)
- Unnamed Classes and Instance Main Methods (JEP 445)
- Foreign Function & Memory API (JEP 442)
- Structured Concurrency (JEP 453)
- Scoped Values (JEP 446)

**Stewardship:**

- Dynamic agent loading produces warnings (JEP 451) - Preparing for future default disallow

### JDK 25 Migration Notes

Source: [Oracle JDK 25 Migration Guide](https://docs.oracle.com/en/java/javase/25/migrate/getting-started.html)

JDK 25 is the next LTS release after JDK 21. The migration guide follows the same structure:

1. Review significant changes in JDK 22-25 releases
2. Check security updates and defaults
3. Verify removed APIs and tools
4. Run `jdeps` and `jdeprscan` against JDK 25
5. Update third-party libraries
6. Test thoroughly before production deployment

**Recommended upgrade path to JDK 25:**

```text
Java 8 → 11 → 17 → 21 → 25
  (LTS)  (LTS)  (LTS)  (LTS)  (LTS)
```
