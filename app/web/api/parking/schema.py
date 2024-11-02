from pydantic import BaseModel
from typing import List, Optional

class MapCoordinatesDTO(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

class ParkingPlaceCreateDTO(BaseModel):
    location: str
    no_of_levels: int

class MapCreateDTO(BaseModel):
    level_no: int
    coordinates: MapCoordinatesDTO

class SlotCreateDTO(BaseModel):
    x1: str
    y1: str
    x2: str
    y2: str
    arduino_ip: Optional[str] = None

class SlotListCreateDTO(BaseModel):
    slots: List[SlotCreateDTO]

class ResponseDTO(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
