CREATE TABLE enrollments (
    enrollment_id    SERIAL PRIMARY KEY,
    employee_id       INTEGER NOT NULL,
    dependent_id       INTEGER,
    eligibility_id      INTEGER NOT NULL,
    plan_code            VARCHAR(20) NOT NULL,
    enrollment_date       DATE NOT NULL,
    coverage_start          DATE NOT NULL,
    coverage_end             DATE,

    CONSTRAINT fk_enrollments_employee
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_enrollments_dependent
        FOREIGN KEY (dependent_id) REFERENCES dependents(dependent_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_enrollments_eligibility
        FOREIGN KEY (eligibility_id) REFERENCES eligibility_determinations(eligibility_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_coverage_end_after_start
        CHECK (coverage_end IS NULL OR coverage_end >= coverage_start)
);

CREATE INDEX idx_enrollments_employee_id ON enrollments(employee_id);
CREATE INDEX idx_enrollments_dependent_id ON enrollments(dependent_id);
CREATE INDEX idx_enrollments_eligibility_id ON enrollments(eligibility_id);
CREATE INDEX idx_enrollments_employee_coverage ON enrollments(employee_id, coverage_start);

COMMENT ON TABLE enrollments IS 'Employee/dependent plan enrollments; every enrollment must trace back to a valid eligibility determination, enforcing the core reconciliation rule';
