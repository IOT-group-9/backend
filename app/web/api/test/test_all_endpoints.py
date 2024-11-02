# test.py

import asyncio
import httpx

BASE_URL = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient() as client:
        # 1. Clear the database
        print("\nClearing the database...")
        response = await client.delete(f"{BASE_URL}/api/test/clear_db")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        # 2. Initialize the database with test data
        print("\nInitializing the database with test data...")
        response = await client.post(f"{BASE_URL}/api/test/init_db")
        print(f"Status Code: {response.status_code}")
        init_data = response.json()
        print(f"Response: {init_data}")

        # Extract IDs for testing
        arduino_ids = init_data["data"]["arduino_ids"]
        parking_place_id = init_data["data"]["parking_place_id"]
        map_ids = init_data["data"]["map_ids"]
        slot_ids = init_data["data"]["slot_ids"]
        display_id = init_data["data"]["display_id"]

        # 3. Test the sensor data endpoint
        print("\nTesting the sensor data endpoint...")

        # Update slot 1 to occupied=True
        sensor_data = {
            "arduino_ip": "192.168.1.10",
            "slot_id": slot_ids[0],
            "occupied": True
        }
        response = await client.post(f"{BASE_URL}/api/sensor/data/receive", json=sensor_data)
        print(f"\nUpdating slot {slot_ids[0]} to occupied=True")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        # Update slot 2 to occupied=True
        sensor_data = {
            "arduino_ip": "192.168.1.11",
            "slot_id": slot_ids[1],
            "occupied": True
        }
        response = await client.post(f"{BASE_URL}/api/sensor/data/receive", json=sensor_data)
        print(f"\nUpdating slot {slot_ids[1]} to occupied=True")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        # 4. Test the parking status endpoint
        print("\nTesting the parking status endpoint...")
        response = await client.get(f"{BASE_URL}/api/parking/places/{parking_place_id}/status")
        print(f"Status Code: {response.status_code}")
        parking_status = response.json()
        print(f"Response: {parking_status}")

        # 5. Test the display status endpoint
        print("\nTesting the display status endpoint...")
        response = await client.get(f"{BASE_URL}/api/display/status/{parking_place_id}")
        print(f"Status Code: {response.status_code}")
        display_status = response.json()
        print(f"Response: {display_status}")

        # 6. Final database state (optional)
        print("\nFinal database state:")
        response = await client.get(f"{BASE_URL}/api/test/db_state")
        db_state = response.json()
        print(db_state)

if __name__ == "__main__":
    asyncio.run(main())
