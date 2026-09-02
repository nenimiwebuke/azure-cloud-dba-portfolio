CREATE TABLE reconciliation_exceptions (
    exception_id      SERIAL PRIMARY KEY,
    employee_id         INTEGER NOT NULL,
    exception_type        VARCHAR(50) NOT NULL,
    detected_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at                TIMESTAMPTZ,
    resolution_notes             TEXT,

    CONSTRAINT fk_reconciliation_employee
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_exception_type
        CHECK (exception_type IN ('enrolled_without_eligibility', 'eligibility_gap', 'duplicate_current_eligibility', 'orphaned_dependent_enrollment')),

    CONSTRAINT chk_resolved_after_detected
        CHECK (resolved_at IS NULL OR resolved_at >= detected_at)
);

CREATE INDEX idx_reconciliation_employee_id ON reconciliation_exceptions(employee_id);

CREATE INDEX idx_reconciliation_unresolved
    ON reconciliation_exceptions(detected_at)
    WHERE resolved_at IS NULL;

COMMENT ON TABLE reconciliation_exceptions IS 'Tracks data quality/reconciliation exceptions detected between eligibility and enrollment records';
