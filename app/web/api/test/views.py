import logging
from fastapi import APIRouter, HTTPException
from app.db.models.models import Arduino, MapSlot, Map, ParkingPlace, Display

logging.basicConfig(level=logging.INFO)
test_router = APIRouter()

@test_router.post("/init_db", tags=["test"])
async def initialize_database():
    try:
        # First, clear existing data
        await clear_database()
        logging.info("Cleared existing data")

        # Add Arduino devices
        arduino_ips = ["192.168.1.10", "192.168.1.11"]
        created_arduinos = []
        
        for ip in arduino_ips:
            arduino = await Arduino.objects().create(
                ip_address=ip
            )
            created_arduinos.append(arduino)
            logging.info(f"Arduino device added with IP: {ip}")

        # Add a single ParkingPlace
        parking_place = await ParkingPlace.objects().create(
            location="Test Parking",
            no_of_levels=2
        )
        logging.info(f"Parking place added with ID: {parking_place.id}")

        # Add Maps for each level
        created_maps = []
        for level in range(1, 3):  # 2 levels
            map_obj = await Map.objects().create(
                parking_place=parking_place.id,
                level_no=level,
                max_x1=0,
                max_y1=0,
                max_x2=100,
                max_y2=100
            )
            created_maps.append(map_obj)
            logging.info(f"Map added for level {level} with ID: {map_obj.id}")

        # Add MapSlots - 2 slots per map, each connected to an Arduino
        created_slots = []
        for map_obj in created_maps:
            for i, arduino in enumerate(created_arduinos):
                slot = await MapSlot.objects().create(
                    map=map_obj.id,
                    x1=i*10,
                    y1="0",
                    x2=(i+1)*10,
                    y2="10",
                    occupied=False,
                    arduino=arduino.id
                )
                created_slots.append(slot)
                logging.info(f"MapSlot added for map {map_obj.id} with Arduino {arduino.id}")

        # Add a Display
        display = await Display.objects().create(
            connection="Test Connection",
            parking_place=parking_place.id
        )
        logging.info(f"Display added with ID: {display.id}")

        # Verify creation by counting objects
        arduino_count = await Arduino.count().run()
        slots_count = await MapSlot.count().run()
        maps_count = await Map.count().run()
        
        logging.info(f"Verification counts - Arduinos: {arduino_count}, "
                    f"Maps: {maps_count}, Slots: {slots_count}")

        return {
            "message": "Database initialized successfully",
            "data": {
                "arduino_ids": [a.id for a in created_arduinos],
                "parking_place_id": parking_place.id,
                "map_ids": [m.id for m in created_maps],
                "slot_ids": [s.id for s in created_slots],
                "display_id": display.id
            },
            "counts": {
                "arduinos": arduino_count,
                "maps": maps_count,
                "slots": slots_count,
                "parking_places": 1,
                "displays": 1
            }
        }
    except Exception as e:
        logging.error(f"An unexpected error occurred during initialization: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during database initialization: {str(e)}"
        )

@test_router.delete("/clear_db")
async def clear_database():
    try:
        # Delete in correct order due to foreign key constraints
        await MapSlot.delete(force=True).run()
        await Display.delete(force=True).run()
        await Map.delete(force=True).run()
        await ParkingPlace.delete(force=True).run()
        await Arduino.delete(force=True).run()
        
        logging.info("All tables cleared successfully")
        return {"message": "Database cleared successfully"}
    except Exception as e:
        logging.error(f"An unexpected error occurred while clearing database: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while clearing database: {str(e)}"
        )


@test_router.get("/db_state", tags=["test"])
async def get_database_state():
    try:
        arduinos = await Arduino.select().run()
        parking_places = await ParkingPlace.select().run()
        maps = await Map.select().run()
        slots = await MapSlot.select().run()
        displays = await Display.select().run()

        return {
            "arduinos": [
                {"id": a["id"], "ip_address": a["ip_address"]} 
                for a in arduinos
            ],
            "parking_places": [
                {
                    "id": p["id"], 
                    "location": p["location"], 
                    "no_of_levels": p["no_of_levels"]
                } 
                for p in parking_places
            ],
            "maps": [
                {
                    "id": m["id"], 
                    "parking_place": m["parking_place"], 
                    "level_no": m["level_no"],
                    "max_x1": m["max_x1"],
                    "max_y1": m["max_y1"],
                    "max_x2": m["max_x2"],
                    "max_y2": m["max_y2"]
                } 
                for m in maps
            ],
            "slots": [
                {
                    "id": s["id"], 
                    "map": s["map"], 
                    "arduino": s["arduino"], 
                    "occupied": s["occupied"],
                    "x1": s["x1"],
                    "y1": s["y1"],
                    "x2": s["x2"],
                    "y2": s["y2"]
                } 
                for s in slots
            ],
            "displays": [
                {
                    "id": d["id"], 
                    "connection": d["connection"], 
                    "parking_place": d["parking_place"]
                } 
                for d in displays
            ]
        }
    except Exception as e:
        logging.error(f"An unexpected error occurred while getting database state: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while getting database state: {str(e)}"
        )
