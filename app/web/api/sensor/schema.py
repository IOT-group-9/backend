from pydantic import BaseModel, IPvAnyAddress
from typing import Optional

class SensorDataInputDTO(BaseModel):
    arduino_ip: str
    slot_id: int
    occupied: bool

class SensorDataDTO(BaseModel):
    success: bool
    message: str

class ArduinoCreateDTO(BaseModel):
    ip_address: str
