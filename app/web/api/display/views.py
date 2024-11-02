import logging
from fastapi import APIRouter, HTTPException
from app.db.models.models import Map, MapSlot, ParkingPlace, Display

logging.basicConfig(level=logging.INFO)
display_router = APIRouter()

@display_router.get("/status/{parking_place_id}")
async def get_display_data(parking_place_id: int):
    try:
        # Verify parking place exists
        parking_place = await ParkingPlace.objects().where(
            ParkingPlace.id == parking_place_id
        ).first().run()
        
        if not parking_place:
            raise HTTPException(status_code=404, detail="Parking place not found")

        # Verify display exists for this parking place
        display = await Display.objects().where(
            Display.parking_place == parking_place_id
        ).first().run()
        
        if not display:
            raise HTTPException(status_code=404, detail="Display not found for this parking place")

        # Get status for each level
        maps = await Map.select(
            Map.id,
            Map.level_no
        ).where(
            Map.parking_place == parking_place_id
        ).order_by(
            Map.level_no
        ).run()

        levels_status = {}
        for map_data in maps:
            available = await MapSlot.count().where(
                (MapSlot.map == map_data["id"]) & 
                (MapSlot.occupied == False)
            ).run()
            
            levels_status[f"Level {map_data['level_no']}"] = available

        return {
            "location": parking_place["location"],
            "available_spaces": levels_status
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
