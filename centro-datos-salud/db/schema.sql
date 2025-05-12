-- db/schema.sql
CREATE TABLE IF NOT EXISTS health_readings (
    sensor_id VARCHAR(50),
    timestamp TIMESTAMP,
    body_temperature DECIMAL(4,1) CHECK (body_temperature > 0),
    heart_rate INTEGER CHECK (heart_rate > 0),
    blood_pressure VARCHAR(15),
    PRIMARY KEY (sensor_id, timestamp)
);
