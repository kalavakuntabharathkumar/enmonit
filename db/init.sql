CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS energy_readings (
    time TIMESTAMPTZ NOT NULL,
    plant TEXT NOT NULL,
    machine_id TEXT NOT NULL,
    power_kw DOUBLE PRECISION NOT NULL,
    voltage_v DOUBLE PRECISION NOT NULL,
    current_a DOUBLE PRECISION NOT NULL,
    temperature_c DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('energy_readings', 'time', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_energy_machine_time
ON energy_readings (machine_id, time DESC);

CREATE INDEX IF NOT EXISTS idx_energy_time_power
ON energy_readings (time DESC, power_kw DESC);
