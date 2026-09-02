CREATE TABLE employment_periods (
    period_id     SERIAL PRIMARY KEY,
    employee_id   INTEGER NOT NULL,
    start_date    DATE NOT NULL,
    end_date      DATE,

    CONSTRAINT fk_employment_periods_employee
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_period_end_after_start
        CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE INDEX idx_employment_periods_employee_id ON employment_periods(employee_id);

COMMENT ON TABLE employment_periods IS 'Tracks distinct employment periods per employee, supporting rehire scenarios for eligibility reconciliation';
