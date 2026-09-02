CREATE TABLE eligibility_determinations (
    eligibility_id      SERIAL PRIMARY KEY,
    employee_id          INTEGER NOT NULL,
    plan_code             VARCHAR(20) NOT NULL,
    eligibility_start      DATE NOT NULL,
    eligibility_end         DATE,
    determination_source  VARCHAR(50) NOT NULL,
    is_current              BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT fk_eligibility_employee
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_eligibility_end_after_start
        CHECK (eligibility_end IS NULL OR eligibility_end >= eligibility_start)
);

CREATE INDEX idx_eligibility_employee_id ON eligibility_determinations(employee_id);

CREATE UNIQUE INDEX idx_eligibility_one_current_per_plan
    ON eligibility_determinations(employee_id, plan_code)
    WHERE is_current = true;

COMMENT ON TABLE eligibility_determinations IS 'Records eligibility determinations per employee per plan; supports the eligibility/enrollment reconciliation scenario';
