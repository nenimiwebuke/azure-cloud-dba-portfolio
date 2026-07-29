# Benefit Plan Data Contract

## Purpose

Defines the benefit plans offered to members through participating employers.

This dataset is considered reference (master) data and is used to validate enrollment and eligibility records.

---

## Primary Key

plan_id

---

## Columns

| Column | Type | Required | Description |
|---------|------|----------|-------------|
| plan_id | STRING | Yes | Unique benefit plan identifier |
| plan_name | STRING | Yes | Business name of the plan |
| plan_type | STRING | Yes | Medical, Dental, Vision, Life, Disability |
| coverage_tier | STRING | Yes | Employee, Employee+Spouse, Employee+Children, Family |
| monthly_premium | DECIMAL(10,2) | Yes | Monthly premium amount |
| deductible | DECIMAL(10,2) | Yes | Annual deductible |
| effective_date | DATE | Yes | Plan effective date |
| termination_date | DATE | No | Plan retirement date |
| plan_status | STRING | Yes | Active or Retired |

---

## Business Rules

1. plan_id must be unique.

2. monthly_premium cannot be negative.

3. deductible cannot be negative.

4. termination_date cannot occur before effective_date.

5. plan_status must be Active or Retired.

6. Active plans cannot have a termination_date in the past.

7. coverage_tier must be one of:
   - Employee
   - Employee+Spouse
   - Employee+Children
   - Family

---

## Data Quality Checks

- Duplicate plan_id
- Missing plan_name
- Invalid plan_type
- Invalid coverage_tier
- Negative premium
- Negative deductible
- Invalid plan_status
- Invalid effective dates

---

## Referential Dependencies

Referenced by:

- Enrollment
- Eligibility
- Gold reporting datasets

