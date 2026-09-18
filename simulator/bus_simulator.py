import time
import random
import requests
import threading
import json
import os
import math
from datetime import datetime


# ==========================================
# API AND OFFLINE STORAGE SETTINGS
# ==========================================

API_URL = "http://127.0.0.1:8000/location"
OFFLINE_FILE = "offline_queue.json"

# Prevent multiple bus threads from changing
# the offline file at the same time.
queue_lock = threading.Lock()


# ==========================================
# OFFLINE STORAGE
# ==========================================

def save_offline(location_data):
    """
    Save a location locally when the network
    is unavailable.
    """

    with queue_lock:

        if os.path.exists(OFFLINE_FILE):

            try:
                with open(OFFLINE_FILE, "r") as file:
                    queue = json.load(file)

            except (json.JSONDecodeError, FileNotFoundError):
                queue = []

        else:
            queue = []

        queue.append(location_data)

        with open(OFFLINE_FILE, "w") as file:
            json.dump(queue, file, indent=4)

    print("💾 Network unavailable. Location saved locally.")


# ==========================================
# SEND LOCATION TO API
# ==========================================

def send_to_api(location_data):
    """
    Try to send one bus location to the API.
    """

    try:

        response = requests.post(
            API_URL,
            json=location_data,
            timeout=5
        )

        if 200 <= response.status_code < 300:

            print("✅ Location sent to API.")
            return True

        print(
            f"⚠️ API returned status: "
            f"{response.status_code}"
        )

        return False

    except requests.exceptions.RequestException:

        print("📴 Network/API unavailable.")
        return False


# ==========================================
# SYNC OFFLINE LOCATIONS
# ==========================================

def sync_offline_locations():
    """
    Try to send locations that were saved
    while the network was unavailable.
    """

    if not os.path.exists(OFFLINE_FILE):
        return

    with queue_lock:

        try:

            with open(OFFLINE_FILE, "r") as file:
                queue = json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):

            queue = []

        if not queue:
            return

        print(
            f"🔄 Syncing {len(queue)} "
            f"offline location(s)..."
        )

        remaining_locations = []

        for location_data in queue:

            try:

                response = requests.post(
                    API_URL,
                    json=location_data,
                    timeout=5
                )

                if 200 <= response.status_code < 300:

                    print(
                        f"☁️ Synced: "
                        f"{location_data['bus_id']}"
                    )

                else:

                    print(
                        f"❌ Sync failed: "
                        f"{location_data['bus_id']}"
                    )

                    remaining_locations.append(
                        location_data
                    )

            except requests.exceptions.RequestException:

                print("📡 Network still unavailable.")

                remaining_locations.append(
                    location_data
                )

        with open(OFFLINE_FILE, "w") as file:

            json.dump(
                remaining_locations,
                file,
                indent=4
            )

        print(
            f"📦 Remaining offline locations: "
            f"{len(remaining_locations)}"
        )


# ==========================================
# BUS DATA
# ==========================================

buses = [

    {
        "bus_id": "BUS-101",

        "route_name":
            "Village A - Village B - Village C - Town",

        "stop": [

            ("Village A", 10.1234, 78.1234),

            ("Village B", 10.1300, 78.1350),

            ("Village C", 10.1400, 78.1500),

            ("Town", 10.1550, 78.1700)
        ]
    },

    {
        "bus_id": "BUS-102",

        "route_name":
            "Village D - Village E - Village F - Town",

        "stop": [

            ("Village D", 10.2000, 78.2000),

            ("Village E", 10.2100, 78.2150),

            ("Village F", 10.2200, 78.2300),

            ("Town", 10.2400, 78.2500)
        ]
    },

    {
        "bus_id": "BUS-103",

        "route_name":
            "Village G - Village H - Village I - Town",

        "stop": [

            ("Village G", 10.3000, 78.3000),

            ("Village H", 10.3100, 78.3150),

            ("Village I", 10.3200, 78.3300),

            ("Town", 10.3400, 78.3500)
        ]
    }
]


# ==========================================
# DISTANCE CALCULATION
# ==========================================

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


# ==========================================
# BUS SIMULATION
# ==========================================

def simulate_bus(bus):

    bus_id = bus["bus_id"]
    route_name = bus["route_name"]
    stops = bus["stop"]

    print(f"\n🚍 {bus_id} started")
    print(f"🛣️ {route_name}")

    # Move from one stop to the next
    for i in range(len(stops) - 1):

        start_name, start_lat, start_lon = stops[i]

        end_name, end_lat, end_lon = stops[i + 1]

        # Number of simulated GPS movements
        steps = 10

        for step in range(steps + 1):

            # ----------------------------------
            # Calculate bus position
            # ----------------------------------

            progress = step / steps

            latitude = (
                start_lat
                + (end_lat - start_lat)
                * progress
            )

            longitude = (
                start_lon
                + (end_lon - start_lon)
                * progress
            )

            # ----------------------------------
            # Current timestamp
            # ----------------------------------

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # ----------------------------------
            # Next stop
            # ----------------------------------

            next_stop = end_name

            # ----------------------------------
            # Distance to next stop
            # ----------------------------------

            distance_km = calculate_distance(
                latitude,
                longitude,
                end_lat,
                end_lon
            )

            # ----------------------------------
            # ETA calculation
            # ----------------------------------

            average_speed_kmh = 30

            eta_minutes = (
                distance_km
                / average_speed_kmh
            ) * 60

           

            # ==================================
            # SIMULATE NETWORK CONDITION
            # ==================================

            network_available = random.choice(
                [
                    True,
                    True,
                    True,
                    False
                ]
            )
            if network_available:
                network_status = "online"
            else:
                network_status = "offline"

            # ----------------------------------
            # Create location data
            # ----------------------------------
            
            location_data = {
            
                            "bus_id": bus_id,
            
                            "route_name": route_name,
            
                            "next_stop": next_stop,
            
                            "eta_minutes":
                                round(eta_minutes, 1),
            
                            "latitude":
                                round(latitude, 6),
            
                            "longitude":
                                round(longitude, 6),
            
                            "timestamp": timestamp,
                            "network_status": network_status
                        }        

            print(
                f"\n🚌 {bus_id} | "
                f"📍 {latitude:.6f}, "
                f"{longitude:.6f}"
            )

            # ==================================
            # NETWORK AVAILABLE
            # ==================================

            if network_available:

                print(
                    f"📡 {bus_id}: "
                    "Network online"
                )

                # First send old locations
                # that were saved offline.
                sync_offline_locations()

                # Then send current location.
                if not send_to_api(location_data):

                    # API failed even though
                    # network was simulated online.
                    save_offline(location_data)

            # ==================================
            # NETWORK UNAVAILABLE
            # ==================================

            else:

                print(
                    f"📡 {bus_id}: "
                    "Network offline"
                )

                save_offline(location_data)

            # Wait before next GPS update
            time.sleep(2)

    print(
        f"🏁 {bus_id} reached destination"
    )


# ==========================================
# MAIN PROGRAM
# ==========================================

print("🚌 Multi-Bus Tracking Simulator")
print("================================")


threads = []


# Start one thread for each bus
for bus in buses:

    thread = threading.Thread(
        target=simulate_bus,
        args=(bus,)
    )

    threads.append(thread)

    thread.start()


# Wait for all buses to finish
for thread in threads:

    thread.join()


print(
    "\n🏁 All buses completed their routes."
)