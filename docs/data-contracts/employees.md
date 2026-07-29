# Employee Data Contract

## Purpose

Contains the authoritative employee population received from employer HR systems.

This dataset represents active and terminated employees eligible for one or more benefit plans.

---

## Primary Key

employee_id

---

## Columns

| Column | Type | Required | Description |
|---------|------|----------|-------------|
| employee_id | STRING | Yes | Unique employee identifier |
| employer_id | STRING | Yes | Employer that owns the employee |
| first_name | STRING | Yes | Employee first name |
| last_name | STRING | Yes | Employee last name |
| date_of_birth | DATE | Yes | Employee birth date |
| hire_date | DATE | Yes | Original hire date |
| termination_date | DATE | No | Employment end date |
| employment_status | STRING | Yes | Active or Terminated |
| department | STRING | Yes | Business department |
| state | STRING | Yes | Employee work state |

---

## Business Rules

1. employee_id must be unique.

2. employer_id must exist in the Employers dataset.

3. Active employees cannot have a termination_date.

4. Terminated employees must have a termination_date.

5. hire_date must occur before termination_date.

6. date_of_birth cannot be in the future.

7. Employees younger than 16 years are rejected.

---

## Data Quality Checks

- Duplicate employee_id
- Missing employer_id
- Invalid state codes
- Invalid employment_status
- Future hire dates
- Future birth dates
- Null first_name
- Null last_name

