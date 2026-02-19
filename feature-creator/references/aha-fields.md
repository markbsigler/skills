# Aha! Standard Fields Reference

## Overview
This reference documents standard Aha! fields and their purposes for feature documentation.

## Core Feature Fields

### Feature Name
- **Purpose:** Unique identifier for the feature
- **Format:** Concise, action-oriented title (3-5 words)
- **Example:** "Multi-user Real-time Collaboration"

### Summary Description
- **Purpose:** High-level overview of what the feature does
- **Length:** 2-3 sentences maximum
- **Focus:** What problem does it solve? What value does it provide?

### Product Area
- **Purpose:** Category/module within the product
- **Example values:** "Core Platform", "Analytics", "Integrations", "Security"

### Release
- **Purpose:** Target release or milestone
- **Example values:** "Q1 2024", "MVP", "Phase 2"

### Priority
- **Purpose:** Relative importance compared to other features
- **Typical values:** Critical, High, Medium, Low

## Business & Strategy Fields

### Business Value Proposition
- **Purpose:** Why this feature matters to the business and users
- **Sections to include:**
  - Revenue impact or cost savings
  - Competitive advantage
  - Customer retention/acquisition benefit
  - Market differentiation

### Use Cases
- **Purpose:** Real-world scenarios where users would benefit from this feature
- **Format:** List of 3-5 concrete, specific scenarios
- **Each use case should:**
  - Start with "As a [user type]..."
  - Include the context and goal
  - Show measurable outcome

### Success Metrics
- **Purpose:** How to measure if the feature achieves its objectives
- **Types:**
  - Adoption metrics (% users, usage frequency)
  - Business metrics (revenue, cost reduction)
  - Quality metrics (error rates, performance)

## Requirements & Implementation Fields

### Requirements
- **Purpose:** Detailed specifications for what the feature must do
- **Format:** EARS format (see ears-format.md)
- **Categories:**
  - Functional requirements
  - Non-functional requirements (performance, security, scalability)
  - User experience requirements

### Acceptance Criteria
- **Purpose:** Clear definition of when the feature is complete
- **Format:** Given-When-Then (BDD format)
- **Characteristics:**
  - Testable and measurable
  - Covers happy path and edge cases
  - Independent of implementation

### Technical Considerations
- **Purpose:** Engineering constraints and dependencies
- **Includes:**
  - Architecture implications
  - API changes or integrations
  - Performance requirements
  - Security/compliance needs

## Related Fields

### Dependencies
- **Purpose:** Other features or work items this depends on
- **Format:** Feature names or IDs

### Acceptance Owner
- **Purpose:** Person responsible for verifying completion
- **Role:** Usually Product Manager or Product Owner

### Theme/Epic
- **Purpose:** Larger strategic initiative this feature supports
- **Example:** "AI-powered Automation Initiative"
