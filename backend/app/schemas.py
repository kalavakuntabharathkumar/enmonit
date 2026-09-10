from datetime import datetime
from pydantic import BaseModel, Field

class SensorReading(BaseModel):
    timestamp: datetime
    plant: str = "Plant-A"
    machine_id: str = "M-01"
    power_kw: float = Field(ge=0)
    voltage_v: float = Field(gt=0)
    current_a: float = Field(ge=0)
    temperature_c: float
