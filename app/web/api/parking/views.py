import logging
from fastapi import APIRouter, HTTPException
from app.db.models.models import Map, MapSlot, ParkingPlace

logging.basicConfig(level=logging.INFO)
parking_router = APIRouter()

@parking_router.get("/places/{parking_place_id}/status")
async def get_parking_status(parking_place_id: int):
    try:
        # Verify parking place exists
        parking_place = await ParkingPlace.objects().where(
            ParkingPlace.id == parking_place_id
        ).first().run()
        
        if not parking_place:
            raise HTTPException(status_code=404, detail="Parking place not found")

        # Get maps for this parking place
        maps = await Map.select(
            Map.id,
            Map.level_no
        ).where(
            Map.parking_place == parking_place_id
        ).order_by(
            Map.level_no
        ).run()

        result = []
        for map_data in maps:
            slots = await MapSlot.select(
                MapSlot.id,
                MapSlot.occupied
            ).where(
                MapSlot.map == map_data["id"]
            ).run()
            
            result.append({
                "level": map_data["level_no"],
                "available_slots": sum(1 for slot in slots if not slot["occupied"]),
                "total_slots": len(slots)
            })

        return {
            "location": parking_place["location"],
            "levels": result
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
