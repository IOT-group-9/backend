import logging
from fastapi import APIRouter, HTTPException
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIWrapper
from app.tkq import broker
from httpx import AsyncClient
from app.settings import settings
from app.db.models.models import Arduino, MapSlot
from .schema import SensorDataInputDTO, SensorDataDTO, ArduinoCreateDTO
from fastapi.responses import Response
from typing import Dict, Any
logging.basicConfig(level=logging.INFO)
sensor_router = APIRouter()

@sensor_router.post("/data/receive", response_model=SensorDataDTO)
async def receive_data(data: SensorDataInputDTO):
    try:
        # Find Arduino by IP Address
        arduino = await Arduino.objects().where(
            Arduino.ip_address == data.arduino_ip
        ).first().run()
        if not arduino:
            raise HTTPException(status_code=404, detail="Arduino not found")

        # Find MapSlot with given slot_id and Arduino reference
        map_slot = await MapSlot.objects().where(
            (MapSlot.id == data.slot_id) &
            (MapSlot.arduino == arduino.id)
        ).first().run()
        if not map_slot:
            raise HTTPException(status_code=404, detail="MapSlot not found")

        # Update occupied status
        await MapSlot.update({
            MapSlot.occupied: data.occupied
        }).where(MapSlot.id == map_slot.id).run()
        await send_publish_request.kiq()

        return SensorDataDTO(success=True, message="Data received and updated successfully")
    except HTTPException as e:
        logging.error(f"HTTPException occurred: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@sensor_router.post("/data/receive_map_slots")
async def receive_data1(data: Dict[Any, Any]):
    try:
        for key, value in data.items():
            await MapSlot.update(
            {MapSlot.occupied: value}
            ).where(MapSlot.id == int(key))
        await send_publish_request.kiq()
        return Response()
    except HTTPException as e:
        logging.error(f"HTTPException occurred: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@sensor_router.get("/data/offline/{device_id}")
async def offline(device_id: str):
    try:
        arduino = await Arduino.objects().get(Arduino.device_id == device_id)
        await MapSlot.update({MapSlot.occupied: "offline"}).where(MapSlot.arduino == arduino)
        await send_publish_request.kiq()
        return Response()
    except HTTPException as e:
        logging.error(f"HTTPException occurred: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# CRUD endpoints for Arduino
FastAPIWrapper(
    root_url="/arduino",
    fastapi_app=sensor_router,
    piccolo_crud=PiccoloCRUD(
        table=Arduino,
        read_only=False,
    ),
)


@broker.task
async def send_publish_request():
    async with AsyncClient() as client:
        await client.get(f"{settings.listening_url}/api/pubsub/publish/1/1")
    return "done!"
