---
name: feature-creator
description: Create comprehensive feature specifications and requirements documents in Aha!-aligned format. Use this skill when building detailed feature descriptions with acceptance criteria, business value, use cases, and EARS-formatted requirements for design and engineering teams.
---

# Feature Creator

## Overview

Transform feature concepts into detailed specifications that align with Aha! standard fields. This skill guides the creation of clear, structured feature documents including summary descriptions, agile user stories, business value propositions, use cases, requirements in EARS format, and acceptance criteria.

## Quick Start

Provide the feature concept and the skill will generate a comprehensive markdown document with:

- **Summary Description** - Concise overview of what the feature does
- **Agile User Story** - Standard format user story
- **Business Value** - Revenue impact, competitive advantage, and customer benefits
- **Use Cases** - Real-world scenarios where users benefit
- **EARS Requirements** - Structured, testable requirements (functional, non-functional, UX)
- **Acceptance Criteria** - BDD-format (Given-When-Then) test scenarios
- **Success Metrics** - How to measure feature success
- **Technical Notes** - Dependencies and implementation considerations

## Creating a Feature Specification

### 1. Gather Feature Information

Start by collecting these inputs from stakeholders:

- **Feature name** - Concise, action-oriented title
- **Core problem** - What user problem does this solve?
- **Target users** - Who benefits from this feature?
- **Success outcomes** - How will we know if this feature succeeds?
- **Technical constraints** - Any known limitations or dependencies

### 2. Reference Standards

This skill includes two key reference documents:

- **[aha-fields.md](aha-fields.md)** - Standard Aha! field definitions and purposes
- **[ears-format.md](ears-format.md)** - EARS (Easy Approach to Requirements Syntax) for writing clear, testable requirements

When writing requirements, use the EARS format patterns:
- "The system shall..." (ubiquitous)
- "When [event], the system shall..." (event-driven)
- "While [state], the system shall..." (state-based)
- "If [condition], the system shall..." (conditional)
- "The system shall not..." (negative/restrictions)

### 3. Use the Feature Template

The skill includes a markdown template at `assets/feature-template.md` with all standard sections. The template structure aligns with Aha! fields and includes:

- Summary description section
- Agile user story format
- Business value proposition sections
- Use cases organization
- Functional and non-functional requirement sections
- BDD-format acceptance criteria
- Success metrics and technical notes

### 4. Structure Your Requirements

Organize requirements into these categories:

**Functional Requirements:**
- What the feature must do
- User interactions and workflows
- Data handling and transformations

**Non-Functional Requirements:**
- Performance thresholds
- Security and privacy
- Scalability and reliability

**User Experience Requirements:**
- UI/UX behaviors
- Feedback and error handling
- Accessibility considerations

### 5. Write Clear Acceptance Criteria

Use the Given-When-Then (BDD) format for acceptance criteria:

```
Given [initial context/state]
When [user performs action]
Then [expected outcome]
```

Example:
```
Given a user is logged in with an empty cart
When they add an item to their cart
Then the cart count should update to 1 and the item should appear in the cart list
```

## Best Practices

- **Be specific**: Replace vague terms ("fast", "reliable") with measurable criteria
- **Focus on value**: Connect requirements to user problems and business outcomes
- **Use consistent language**: Define terms and maintain consistent terminology throughout
- **Cover edge cases**: Include acceptance criteria for error states and boundary conditions
- **Link to Aha!**: Ensure all sections map to Aha! standard fields for seamless integration

## Resources

### references/aha-fields.md
Comprehensive reference of standard Aha! fields including core feature fields (Name, Summary, Product Area, Release, Priority), business & strategy fields (Value Proposition, Use Cases, Success Metrics), and requirements fields (Requirements, Acceptance Criteria, Technical Considerations). Use this when you need to understand how to populate specific Aha! fields or what information each field should contain.

### references/ears-format.md
Complete guide to EARS (Easy Approach to Requirements Syntax) including the five requirement types (Ubiquitous, Event-Driven, State-Based, Conditional, Negative) with templates and examples. Reference this when writing the requirements section to ensure clear, testable requirement statements.

### assets/feature-template.md
Ready-to-use markdown template with all standard sections pre-structured. Copy this template and fill in the sections for each new feature. The template includes prompts for each section to guide content creation.
