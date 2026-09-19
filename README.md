# 🚌 Rural Bus Tracking System

## 📌 Project Overview

A real-time rural bus tracking system designed to help passengers
track buses, view their current location, next stop, estimated
arrival time, and route history.

The system simulates GPS-enabled buses and demonstrates how location
data can be collected, stored, processed, and displayed through a
web-based map.

## 🎯 Problem Statement

Passengers in rural areas may have limited information about bus
locations and arrival times.

This project demonstrates a solution where bus location information
can be sent to a backend API and displayed on a live map.

## 💡 Solution

The system contains three main components:

- Python bus simulator
- FastAPI backend
- Leaflet web frontend

The simulator generates bus GPS locations and sends them to the
FastAPI backend. The backend stores the information in SQLite.
The frontend retrieves the latest information and displays the
buses on an interactive map.

## 🏗️ Architecture 

                    ┌──────────────────────┐
                    │   Bus Simulator      │
                    │   Python             │
                    │                      │
                    │ GPS + ETA + Network  │
                    └──────────┬───────────┘
                               │
                         HTTP POST
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI          │
                    │      Backend         │
                    │                      │
                    │ /location            │
                    │ /bus/{bus_id}        │
                    │ /history             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       SQLite         │
                    │   bus_tracking.db    │
                    │                      │
                    │ Location History     │
                    └──────────┬───────────┘
                               │
                         REST API
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Web Frontend      |
                    │ HTML + JavaScript    |
                    │      Leaflet         |
                    │                      |
                    │ 🚌 Live Markers      |
                    │ 📍 Next Stop         |
                    │ ⏱️ ETA               |
                    │ 🛣️ Route History     |
                    └──────────────────────┘
                         Network Failure
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Offline Queue       │
                    │ offline_queue.json  │
                    └──────────┬──────────┘
                               │
                         Network returns
                               │
                               ▼
                          Automatic Sync
                  

                       

 Bus Simulator
 ↓
 FastAPI REST API
 ↓
 SQLite Database
 ↓
 Leaflet Web Map

 During network failure:

 Bus Simulator
 ↓
 Offline Queue
 ↓
 Network Recovery
 ↓
 Automatic Synchronization
 ↓
 FastAPI
 ↓
 SQLite

## ✨ Features

- 🚌 Multiple bus simulation
- 📍 GPS location simulation
- ⏱️ ETA calculation
- 🚏 Next-stop information
- 🗺️ Interactive map
- 🔎 Bus selection
- 🛣️ Route history
- 📡 Network availability simulation
- 💾 Offline location storage
- 🔄 Automatic synchronization
- 🗄️ SQLite location database
- ⚡ FastAPI REST API

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Bus simulation and logic |
| FastAPI | Backend REST API |
| SQLite | Location data storage |
| HTML | Frontend structure |
| JavaScript | Frontend logic |
| Leaflet | Interactive map |
| OpenStreetMap | Map tiles |
| Requests | API communication |
| Git/GitHub | Version control |

## 📁 Project Structure

  rural-bus-tracker/
  │
  ├── backend/
  │   ├── main.py
  │   └── database.py
  │
  ├── simulator/
  │   └── bus_simulator.py
  │
  ├── frontend/
  │   └── index.html
  │
  ├── requirements.txt
  ├── .gitignore
  └── README.md

## 🚀 How to Run

### 1. Install dependencies

pip install -r requirements.txt

### 2. Start the FastAPI backend

python -m uvicorn backend.main:app --reload

### 3. Start the bus simulator

python simulator/bus_simulator.py

### 4. Open the frontend

Open:

frontend/index.html

in a browser.

## 🔌 API Endpoints

### GET /

Checks whether the API is running.

### POST /location

Receives a bus location from the simulator.

### GET /bus/{bus_id}

Returns the latest location of a bus.

### GET /bus/{bus_id}/history

Returns the location history of a bus.

## 📡 Offline Handling

When network connectivity is simulated as unavailable, the bus
location is stored locally in:

offline_queue.json

When connectivity becomes available again, the simulator attempts
to synchronize the stored locations with the backend.

## 🧪 Testing

The following tests were completed successfully:

- [x] FastAPI backend
- [x] SQLite database
- [x] Multiple buses
- [x] GPS simulation
- [x] ETA calculation
- [x] Bus selection
- [x] Live map markers
- [x] Route history
- [x] Offline queue
- [x] Offline synchronization
- [x] Network status
- [x] API communication

## 📸 Screenshots

### 🚌 Rural Bus Tracker

![Rural Bus Tracker]
<img width="1366" height="768" alt="Screenshot (20)" src="https://github.com/user-attachments/assets/ec619372-d096-4b3c-adc4-9803fc1647e3" />



### 📚 FastAPI Documentation

![FastAPI Documentation]
<img width="1366" height="681" alt="Screenshot (22)" src="https://github.com/user-attachments/assets/3895cbb8-af93-4c39-8f01-de1a42a46d6a" />


## ⚠️ Current Limitations

This project currently uses simulated GPS coordinates rather than
physical GPS devices.

The map displays simulated routes rather than actual road paths.

The system is intended as a working prototype and demonstration
of the architecture.

## 🔮 Future Improvements

- Real GPS hardware integration
- Cloud deployment
- User authentication
- Real road routing
- Mobile application
- Push notifications
- Passenger-specific bus alerts
- Production database
- Monitoring and logging

## 👨‍💻 Project Goal

This project demonstrates practical implementation of:

Python automation, REST APIs, backend development, database
management, GPS data processing, offline handling, and
interactive web mapping.
