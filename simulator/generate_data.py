import argparse
import math
import random
from datetime import datetime, timezone, timedelta
import psycopg

DB = "postgresql://energy:energy@db:5432/energy"

def generate(seconds: int):
    start = datetime.now(timezone.utc).replace(microsecond=0)
    rows = []
    for i in range(seconds):
        timestamp = start + timedelta(seconds=i)
        power = 120 + 18 * math.sin(i / 30) + random.uniform(-5, 5)
        if i and i % 600 == 0:
            power += 80
        voltage = 415 + random.uniform(-2, 2)
        current = max(1, power * 1000 / (voltage * 1.732))
        temperature = 58 + power / 40 + random.uniform(-1.5, 1.5)
        rows.append(
            (timestamp, "Plant-A", "M-01", power, voltage, current, temperature)
        )

    with psycopg.connect(DB) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """INSERT INTO energy_readings
                (time, plant, machine_id, power_kw, voltage_v, current_a, temperature_c)
                VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                rows,
            )
    print(f"Inserted {len(rows)} readings.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=3600)
    generate(parser.parse_args().seconds)
