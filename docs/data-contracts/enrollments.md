# Enrollment Data Contract

## Purpose

Represents benefit plan elections submitted by employer HR systems.

Enrollment records are used to establish requested member coverage before reconciliation with the eligibility system.

---

## Primary Key

enrollment_id

---

## Columns

| Column | Type | Required | Description |
|---------|------|----------|-------------|
| enrollment_id | STRING | Yes | Unique enrollment record identifier |
| employer_id | STRING | Yes | Employer submitting the enrollment |
| employee_id | STRING | Yes | Employee requesting coverage |
| dependent_id | STRING | No | Covered dependent (if applicable) |
| plan_id | STRING | Yes | Selected benefit plan |
| coverage_start_date | DATE | Yes | Requested coverage start |
| coverage_end_date | DATE | No | Coverage termination |
| enrollment_status | STRING | Yes | Active, Pending, Cancelled |
| source_file_name | STRING | Yes | Original inbound file |
| source_received_timestamp | TIMESTAMP | Yes | Time file was received |

---

## Business Rules

1. enrollment_id must be unique.

2. employer_id must exist in Employers.

3. employee_id must exist in Employees.

4. plan_id must exist in Plans.

5. coverage_start_date cannot occur before the employee hire_date.

6. coverage_end_date cannot occur before coverage_start_date.

7. Cancelled enrollments cannot produce eligibility.

8. Duplicate active enrollments for the same employee and plan are not permitted.

9. Pending enrollments cannot be used for claims validation.

---

## Data Quality Checks

- Duplicate enrollment_id
- Unknown employer_id
- Unknown employee_id
- Unknown plan_id
- Invalid enrollment_status
- Coverage before hire date
- Invalid coverage period
- Missing source file metadata

---

## Referential Dependencies

Referenced by:

- Eligibility reconciliation
- Claims validation
- Gold reporting
