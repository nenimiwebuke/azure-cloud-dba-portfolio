# Dependent Data Contract

## Purpose

Represents spouses and children enrolled under an employee's benefit coverage.

Dependents are linked to a primary employee (subscriber) and may be covered under one or more benefit plans.

---

## Primary Key

dependent_id

---

## Columns

| Column | Type | Required | Description |
|---------|------|----------|-------------|
| dependent_id | STRING | Yes | Unique dependent identifier |
| employee_id | STRING | Yes | Primary employee (subscriber) |
| first_name | STRING | Yes | Dependent first name |
| last_name | STRING | Yes | Dependent last name |
| relationship | STRING | Yes | Spouse, Child, Domestic Partner |
| date_of_birth | DATE | Yes | Dependent birth date |
| gender | STRING | Yes | M or F |
| dependent_status | STRING | Yes | Active or Terminated |

---

## Business Rules

1. dependent_id must be unique.

2. employee_id must exist in Employees.

3. relationship must be one of:
   - Spouse
   - Child
   - Domestic Partner

4. Children cannot be older than the employee.

5. Active dependents cannot belong to terminated employees unless continuation coverage exists.

6. date_of_birth cannot be in the future.

7. dependent_status must be Active or Terminated.

---

## Data Quality Checks

- Duplicate dependent_id
- Unknown employee_id
- Invalid relationship
- Invalid dependent_status
- Future birth dates
- Child older than subscriber

---

## Referential Dependencies

Referenced by:

- Enrollment
- Eligibility
- Claims

