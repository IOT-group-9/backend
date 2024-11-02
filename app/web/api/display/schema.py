from pydantic import BaseModel

class CreateDisplayDTO(BaseModel):
    connection: str
    parking_place_id: int
