from datetime import datetime, timezone
from backend.app.schemas import SensorReading

def test_reading_schema():
    r = SensorReading(
        timestamp=datetime.now(timezone.utc),
        power_kw=125.5,
        voltage_v=415,
        current_a=180,
        temperature_c=61,
    )
    assert r.power_kw == 125.5
