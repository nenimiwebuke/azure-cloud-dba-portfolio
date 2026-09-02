CREATE TABLE employees (
    employee_id       SERIAL PRIMARY KEY,
    employee_number   VARCHAR(20) NOT NULL UNIQUE,
    first_name        VARCHAR(50) NOT NULL,
    last_name         VARCHAR(50) NOT NULL,
    hire_date         DATE NOT NULL,
    termination_date  DATE,
    employment_status VARCHAR(20) NOT NULL DEFAULT 'active',

    CONSTRAINT chk_employment_status
        CHECK (employment_status IN ('active', 'terminated', 'on_leave')),

    CONSTRAINT chk_termination_after_hire
        CHECK (termination_date IS NULL OR termination_date >= hire_date)
);

CREATE INDEX idx_employees_status ON employees(employment_status);

COMMENT ON TABLE employees IS 'Core workforce record for Northstar eligibility/employment reconciliation scenario';
