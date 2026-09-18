import sqlite3

DATABASE_NAME = "bus_tracking.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Create the table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_id TEXT NOT NULL,
            route_name TEXT NOT NULL,
            next_stop TEXT NOT NULL,
            eta_minutes REAL NOT NULL DEFAULT 0,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            timestamp TEXT NOT NULL,
            network_status TEXT NOT NULL DEFAULT 'unknown'
        )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(bus_locations)")

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # Add eta_minutes if an older database does not have it
    if "eta_minutes" not in columns:

        cursor.execute("""
            ALTER TABLE bus_locations
            ADD COLUMN eta_minutes REAL NOT NULL DEFAULT 0
        """)

    # Add network_status if an older database does not have it
    if "network_status" not in columns:

        cursor.execute("""
            ALTER TABLE bus_locations
            ADD COLUMN network_status TEXT NOT NULL DEFAULT 'unknown'
        """)

    connection.commit()
    connection.close()


def save_location(
    bus_id,
    route_name,
    next_stop,
    eta_minutes,
    latitude,
    longitude,
    timestamp,
    network_status
):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO bus_locations
        (
            bus_id,
            route_name,
            next_stop,
            eta_minutes,
            latitude,
            longitude,
            timestamp,
            network_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        bus_id,
        route_name,
        next_stop,
        eta_minutes,
        latitude,
        longitude,
        timestamp,
        network_status
    ))

    connection.commit()
    connection.close()


def get_latest_location(bus_id):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bus_id,
            route_name,
            next_stop,
            eta_minutes,
            latitude,
            longitude,
            timestamp,
            network_status
        FROM bus_locations
        WHERE bus_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (bus_id,))

    result = cursor.fetchone()

    connection.close()

    return result


def get_location_history(bus_id):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            bus_id,
            route_name,
            next_stop,
            eta_minutes,
            latitude,
            longitude,
            timestamp,
            network_status
        FROM bus_locations
        WHERE bus_id = ?
        ORDER BY id ASC
    """, (bus_id,))

    results = cursor.fetchall()

    connection.close()

    return results