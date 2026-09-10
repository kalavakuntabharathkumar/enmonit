from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Query
from .db import get_connection
from .schemas import SensorReading

app = FastAPI(title="Industrial Energy Monitoring API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/readings", status_code=201)
def ingest(reading: SensorReading):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO energy_readings
                (time, plant, machine_id, power_kw, voltage_v, current_a, temperature_c)
                VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (reading.timestamp, reading.plant, reading.machine_id,
                 reading.power_kw, reading.voltage_v,
                 reading.current_a, reading.temperature_c),
            )
    return {"inserted": True}

@app.get("/api/readings/latest")
def latest(limit: int = Query(100, ge=1, le=5000)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT time, plant, machine_id, power_kw, voltage_v,
                          current_a, temperature_c
                   FROM energy_readings
                   ORDER BY time DESC LIMIT %s""",
                (limit,),
            )
            return cur.fetchall()

@app.get("/api/readings/summary")
def summary(hours: int = Query(1, ge=1, le=168)):
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT count(*) AS samples,
                          round(avg(power_kw)::numeric,2) AS avg_power_kw,
                          round(max(power_kw)::numeric,2) AS peak_power_kw,
                          round(avg(temperature_c)::numeric,2) AS avg_temperature_c
                   FROM energy_readings WHERE time >= %s""",
                (since,),
            )
            return cur.fetchone()
