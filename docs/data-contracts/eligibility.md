# Eligibility Data Contract

## Purpose

Represents the authoritative member eligibility maintained by the benefits administration platform.

Eligibility determines whether a member is entitled to receive benefits on a given service date.

---

## Primary Key

eligibility_id

---

## Columns

| Column | Type | Required | Description |
|---------|------|----------|-------------|
| eligibility_id | STRING | Yes | Unique eligibility record identifier |
| employee_id | STRING | Yes | Employee receiving coverage |
| dependent_id | STRING | No | Covered dependent (if applicable) |
| plan_id | STRING | Yes | Approved benefit plan |
| eligibility_start_date | DATE | Yes | Coverage effective date |
| eligibility_end_date | DATE | No | Coverage termination date |
| eligibility_status | STRING | Yes | Active, Pending, Terminated |
| approval_timestamp | TIMESTAMP | Yes | Time eligibility became effective |
| source_system | STRING | Yes | Originating eligibility platform |

---

## Business Rules

1. eligibility_id must be unique.

2. employee_id must exist in Employees.

3. plan_id must exist in Plans.

4. eligibility_start_date cannot occur before employee hire_date.

5. eligibility_end_date cannot occur before eligibility_start_date.

6. Active eligibility cannot have an end date in the past.

7. Pending eligibility cannot be used for claims processing.

8. There cannot be overlapping active eligibility periods for the same employee and plan.

9. source_system cannot be null.

---

## Data Quality Checks

- Duplicate eligibility_id
- Unknown employee_id
- Unknown plan_id
- Invalid eligibility_status
- Invalid eligibility dates
- Missing source_system
- Overlapping active eligibility periods

---

## Referential Dependencies

Referenced by:

- Claims validation
- Eligibility reconciliation
- Gold reporting
- Coverage analytics

