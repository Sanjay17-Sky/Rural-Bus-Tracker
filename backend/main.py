from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database import (
    create_database,
    save_location,
    get_latest_location,
    get_location_history
)


app = FastAPI(title="Rural Bus Tracking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


class BusLocation(BaseModel):

    bus_id: str
    route_name: str
    next_stop: str
    eta_minutes: float
    latitude: float
    longitude: float
    timestamp: str
    network_status: str


create_database()


@app.get("/")
def home():

    return {
        "message": "Rural Bus Tracking API is running"
    }


@app.post("/location")
def receive_location(location: BusLocation):

    save_location(
        location.bus_id,
        location.route_name,
        location.next_stop,
        location.eta_minutes,
        location.latitude,
        location.longitude,
        location.timestamp,
        location.network_status
    )

    return {
        "message": "Location saved successfully",
        "data": location
    }


@app.get("/bus/{bus_id}")
def get_bus(bus_id: str):

    location = get_latest_location(bus_id)

    if location is None:

        return {
            "message": "Bus not found"
        }

    return {
        "bus_id": location[0],
        "route_name": location[1],
        "next_stop": location[2],
        "eta_minutes": location[3],
        "latitude": location[4],
        "longitude": location[5],
        "timestamp": location[6],
        "network_status": location[7]
    }
@app.get("/bus/{bus_id}/history")
def get_bus_history(bus_id: str):

    locations = get_location_history(bus_id)

    if not locations:

        return {
            "message": "No location history found"
        }

    history = []

    for location in locations:

        history.append({
            "bus_id": location[0],
            "route_name" : location[1],
            "next_stop": location[2],
            "eta_minutes": location[3],
            "latitude": location[4],
            "longitude": location[5],
            "timestamp": location[6],
            "network_status": location[7]
        })

    return {
        "bus_id": bus_id,
        "total_locations": len(history),
        "locations": history
    }