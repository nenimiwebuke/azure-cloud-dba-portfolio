CREATE TABLE dependents (
    dependent_id      SERIAL PRIMARY KEY,
    employee_id       INTEGER NOT NULL,
    first_name        VARCHAR(50) NOT NULL,
    last_name         VARCHAR(50) NOT NULL,
    relationship_type VARCHAR(20) NOT NULL,
    date_of_birth     DATE NOT NULL,

    CONSTRAINT fk_dependents_employee
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_relationship_type
        CHECK (relationship_type IN ('spouse', 'child', 'domestic_partner'))
);

CREATE INDEX idx_dependents_employee_id ON dependents(employee_id);

COMMENT ON TABLE dependents IS 'Dependents eligible for coverage under an employee, used in enrollment and eligibility reconciliation';
