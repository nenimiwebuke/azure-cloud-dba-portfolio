-- Employees
INSERT INTO employees (employee_number, first_name, last_name, hire_date, employment_status) VALUES
    ('EMP-1001', 'Maria', 'Chen', '2022-03-15', 'active'),
    ('EMP-1002', 'James', 'Okafor', '2021-07-01', 'active'),
    ('EMP-1003', 'Priya', 'Nair', '2023-01-10', 'active'),
    ('EMP-1004', 'David', 'Kim', '2019-11-20', 'terminated');

-- Update David's termination date now that his row exists
UPDATE employees
SET termination_date = '2025-06-30'
WHERE employee_number = 'EMP-1004';

-- Employment periods
INSERT INTO employment_periods (employee_id, start_date, end_date)
SELECT employee_id, hire_date, termination_date
FROM employees;

-- Dependents
INSERT INTO dependents (employee_id, first_name, last_name, relationship_type, date_of_birth)
SELECT employee_id, 'Alex', 'Chen', 'spouse', '1990-05-12'
FROM employees WHERE employee_number = 'EMP-1001';

INSERT INTO dependents (employee_id, first_name, last_name, relationship_type, date_of_birth)
SELECT employee_id, 'Sam', 'Chen', 'child', '2015-08-22'
FROM employees WHERE employee_number = 'EMP-1001';

INSERT INTO dependents (employee_id, first_name, last_name, relationship_type, date_of_birth)
SELECT employee_id, 'Ngozi', 'Okafor', 'spouse', '1985-02-03'
FROM employees WHERE employee_number = 'EMP-1002';

-- Eligibility determinations (all current)
INSERT INTO eligibility_determinations (employee_id, plan_code, eligibility_start, determination_source, is_current)
SELECT employee_id, 'MEDICAL-PPO', hire_date, 'benefits_engine_v2', true
FROM employees WHERE employment_status = 'active';

INSERT INTO eligibility_determinations (employee_id, plan_code, eligibility_start, determination_source, is_current)
SELECT employee_id, 'DENTAL-STD', hire_date, 'benefits_engine_v2', true
FROM employees WHERE employment_status = 'active';

-- Enrollments (must reference a valid eligibility_id)
INSERT INTO enrollments (employee_id, dependent_id, eligibility_id, plan_code, enrollment_date, coverage_start)
SELECT e.employee_id, NULL, el.eligibility_id, 'MEDICAL-PPO', e.hire_date, e.hire_date
FROM employees e
JOIN eligibility_determinations el ON el.employee_id = e.employee_id AND el.plan_code = 'MEDICAL-PPO'
WHERE e.employment_status = 'active';

-- One dependent enrollment (Maria's spouse Alex, on her medical plan)
INSERT INTO enrollments (employee_id, dependent_id, eligibility_id, plan_code, enrollment_date, coverage_start)
SELECT e.employee_id, d.dependent_id, el.eligibility_id, 'MEDICAL-PPO', e.hire_date, e.hire_date
FROM employees e
JOIN dependents d ON d.employee_id = e.employee_id AND d.relationship_type = 'spouse'
JOIN eligibility_determinations el ON el.employee_id = e.employee_id AND el.plan_code = 'MEDICAL-PPO'
WHERE e.employee_number = 'EMP-1001';
