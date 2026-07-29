# Employer Data Contract

## Purpose

Contains the authoritative employer-group records used to identify organizations participating in the benefits platform.

Each employer may submit employee, dependent, enrollment, and eligibility data according to an agreed delivery schedule.

---

## Primary Key

employer_id

---

## Columns

| Column | Type | Required | Description |
|---------|------|----------|-------------|
| employer_id | STRING | Yes | Unique employer identifier |
| employer_name | STRING | Yes | Legal or recognized employer name |
| industry | STRING | Yes | Employer industry classification |
| state | STRING | Yes | Employer headquarters state |
| contract_start_date | DATE | Yes | Benefits administration contract start date |
| contract_end_date | DATE | No | Benefits administration contract end date |
| account_status | STRING | Yes | Active, Suspended, or Terminated |
| expected_file_frequency | STRING | Yes | Daily, Weekly, Biweekly, or Monthly |
| source_system | STRING | Yes | Originating employer or partner system |
| last_updated_timestamp | TIMESTAMP | Yes | Most recent source-system update timestamp |

---

## Business Rules

1. employer_id must be unique.

2. employer_name cannot be null or blank.

3. state must be a valid two-character United States state code.

4. contract_start_date is required.

5. contract_end_date cannot occur before contract_start_date.

6. Active employers should not have a contract_end_date in the past.

7. Terminated employers must have a contract_end_date.

8. account_status must be one of:
   - Active
   - Suspended
   - Terminated

9. expected_file_frequency must be one of:
   - Daily
   - Weekly
   - Biweekly
   - Monthly

10. source_system cannot be null or blank.

11. last_updated_timestamp cannot be in the future beyond an approved clock-skew tolerance.

---

## Data Quality Checks

- Duplicate employer_id
- Missing employer_name
- Invalid state code
- Invalid account_status
- Invalid expected_file_frequency
- Missing contract_start_date
- Contract end date before contract start date
- Active employer with an expired contract
- Terminated employer without a contract_end_date
- Missing source_system
- Future last_updated_timestamp

---

## Referential Dependencies

The following datasets reference employer_id:

- Employees
- Enrollment files
- File-ingestion audit records
- Employer reconciliation outputs
