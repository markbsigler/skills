# EARS Format Reference

## Overview

EARS (Easy Approach to Requirements Syntax) is a standardized way to write clear, testable requirements. It uses structured sentences with consistent keywords.

## Core EARS Template

```
<Keyword> <optional precondition>
  <Requirement subject> <action> <object> [<optional postCondition>]
```

## Five EARS Requirement Types

### 1. Ubiquitous Requirements (always apply)

**Template:** `The <system> shall <action>`

**Usage:** Requirements that have no conditions - they always apply.

**Examples:**
- "The system shall store all user preferences securely"
- "The system shall validate email format before accepting input"
- "The system shall maintain audit logs of all administrative actions"

### 2. Event-Driven Requirements (triggered by events)

**Template:** `When <event>, the <system> shall <action>`

**Usage:** Requirements triggered by specific events or user actions.

**Examples:**
- "When a user logs in, the system shall display their dashboard"
- "When a file exceeds 100MB, the system shall notify the user"
- "When inventory drops below threshold, the system shall trigger a purchase order"

### 3. State-Based Requirements (dependent on system state)

**Template:** `While <state>, the <system> shall <action>`

**Usage:** Requirements that apply only in certain system states.

**Examples:**
- "While the user is offline, the system shall queue transactions locally"
- "While in debug mode, the system shall log all API calls"
- "While storage is above 90%, the system shall alert administrators"

### 4. Conditional Requirements (if/then logic)

**Template:** `If <condition>, the <system> shall <action>`

**Usage:** Requirements with specific conditions that must be met.

**Examples:**
- "If the user has admin privileges, the system shall display the admin panel"
- "If payment fails, the system shall retry automatically after 5 minutes"
- "If duplicate email is detected, the system shall prompt user to merge accounts"

### 5. Negative Requirements (what must NOT happen)

**Template:** `The <system> shall not <action>`

**Usage:** Explicit restrictions or prohibited behaviors.

**Examples:**
- "The system shall not allow users to delete data older than 30 days"
- "The system shall not expose sensitive user data in error messages"
- "The system shall not process payments without SSL encryption"

## Writing Effective EARS Requirements

### Best Practices

1. **One requirement per statement** - Each EARS sentence should describe a single, testable requirement
2. **Use active voice** - "The system shall do X" not "X should be done"
3. **Be specific** - Use concrete terms; avoid vague language like "fast," "reliable," or "appropriate"
4. **Make it testable** - Every requirement should have observable, measurable acceptance criteria
5. **Use consistent terminology** - Define terms and use them consistently throughout

### Avoid These Mistakes

- ❌ "The system should be user-friendly" → ✅ "The system shall complete user login in under 2 seconds"
- ❌ "The system might support exports" → ✅ "When user clicks Export, the system shall generate a CSV file"
- ❌ "The feature is important" → ✅ "When a user creates a report, the system shall save it automatically"
- ❌ "The system shall do several things" → ✅ Break into individual EARS statements

## EARS Requirements in Aha! Features

When documenting a feature in Aha!, use the EARS format to organize requirements into these categories:

### Functional Requirements
Requirements describing what the feature must do:
```
When user clicks [button], the system shall [action]
The system shall [perform action]
If [condition], the system shall [action]
```

### Non-Functional Requirements
Requirements for performance, security, scalability:
```
The system shall process [action] in under [X] seconds
The system shall encrypt all [data type] using [standard]
The system shall support at least [X] concurrent users
```

### User Experience Requirements
Requirements for usability and interface:
```
While in [state], the system shall display [element]
The system shall not [prohibit action] without [confirmation]
When [user action], the system shall provide [feedback] within [X] seconds
```

## Example Feature Requirements in EARS

Feature: "Search with Filters"

**Functional:**
- When user enters search text, the system shall display matching results in under 1 second
- When user selects a filter, the system shall update results to show only matching items
- If no results match, the system shall display "No results found"
- The system shall not process searches with special characters without escaping

**Non-Functional:**
- The system shall support searches on datasets up to 1 million records
- The system shall cache search results for 5 minutes
- The system shall encrypt search queries in transit using TLS 1.3

**UX:**
- While results are loading, the system shall display a loading spinner
- When user clears filters, the system shall restore the original full result set
- The system shall highlight matching search terms in the results
