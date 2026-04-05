from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Fleet Service",
    description="Manages delivery vehicles in the Courier System",
    version="1.0.0"
)

# In-memory database
vehicles = []
counter = {"id": 1}

# ---------- Models ----------
class Vehicle(BaseModel):
    vehicle_number: str
    vehicle_type: str  # BIKE, VAN, TRUCK
    driver_name: str
    driver_phone: str
    capacity_kg: float
    status: Optional[str] = "AVAILABLE"  # AVAILABLE, ON_DELIVERY, MAINTENANCE

class VehicleResponse(Vehicle):
    id: int

# ---------- Routes ----------
@app.get("/", tags=["Health"])
def root():
    return {"service": "Fleet Service", "status": "running"}

@app.get("/fleet", response_model=List[VehicleResponse], tags=["Fleet"])
def get_all_vehicles():
    """Get all vehicles"""
    return vehicles

@app.get("/fleet/{vehicle_id}", response_model=VehicleResponse, tags=["Fleet"])
def get_vehicle(vehicle_id: int):
    """Get a vehicle by ID"""
    for v in vehicles:
        if v["id"] == vehicle_id:
            return v
    raise HTTPException(status_code=404, detail="Vehicle not found")

@app.get("/fleet/available/list", response_model=List[VehicleResponse], tags=["Fleet"])
def get_available_vehicles():
    """Get all vehicles with AVAILABLE status"""
    return [v for v in vehicles if v["status"] == "AVAILABLE"]

@app.post("/fleet", response_model=VehicleResponse, status_code=201, tags=["Fleet"])
def add_vehicle(vehicle: Vehicle):
    """Add a new vehicle to the fleet"""
    new = {"id": counter["id"], **vehicle.dict()}
    vehicles.append(new)
    counter["id"] += 1
    return new

@app.put("/fleet/{vehicle_id}", response_model=VehicleResponse, tags=["Fleet"])
def update_vehicle(vehicle_id: int, vehicle: Vehicle):
    """Update vehicle details"""
    for i, v in enumerate(vehicles):
        if v["id"] == vehicle_id:
            vehicles[i] = {"id": vehicle_id, **vehicle.dict()}
            return vehicles[i]
    raise HTTPException(status_code=404, detail="Vehicle not found")

@app.patch("/fleet/{vehicle_id}/status", response_model=VehicleResponse, tags=["Fleet"])
def update_vehicle_status(vehicle_id: int, status: str):
    """Update vehicle status (AVAILABLE, ON_DELIVERY, MAINTENANCE)"""
    valid_statuses = ["AVAILABLE", "ON_DELIVERY", "MAINTENANCE"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    for i, v in enumerate(vehicles):
        if v["id"] == vehicle_id:
            vehicles[i]["status"] = status
            return vehicles[i]
    raise HTTPException(status_code=404, detail="Vehicle not found")

@app.delete("/fleet/{vehicle_id}", tags=["Fleet"])
def delete_vehicle(vehicle_id: int):
    """Remove a vehicle from the fleet"""
    for i, v in enumerate(vehicles):
        if v["id"] == vehicle_id:
            vehicles.pop(i)
            return {"message": f"Vehicle {vehicle_id} removed successfully"}
    raise HTTPException(status_code=404, detail="Vehicle not found")
