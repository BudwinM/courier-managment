from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Hub Service",
    description="Manages distribution hubs and parcel sorting in the Courier System",
    version="1.0.0"
)

# In-memory database
hubs = []
hub_counter = {"id": 1}

parcels_at_hub = []
parcel_counter = {"id": 1}

# ---------- Models ----------
class Hub(BaseModel):
    name: str
    city: str
    address: str
    contact_number: str
    capacity: int  # max number of parcels

class HubResponse(Hub):
    id: int

class HubParcel(BaseModel):
    hub_id: int
    order_id: int
    status: Optional[str] = "RECEIVED"  # RECEIVED, SORTED, DISPATCHED

class HubParcelResponse(HubParcel):
    id: int

# ---------- Hub Routes ----------
@app.get("/", tags=["Health"])
def root():
    return {"service": "Hub Service", "status": "running"}

@app.get("/hubs", response_model=List[HubResponse], tags=["Hubs"])
def get_all_hubs():
    """Get all distribution hubs"""
    return hubs

@app.get("/hubs/{hub_id}", response_model=HubResponse, tags=["Hubs"])
def get_hub(hub_id: int):
    """Get a hub by ID"""
    for h in hubs:
        if h["id"] == hub_id:
            return h
    raise HTTPException(status_code=404, detail="Hub not found")

@app.post("/hubs", response_model=HubResponse, status_code=201, tags=["Hubs"])
def create_hub(hub: Hub):
    """Create a new distribution hub"""
    new = {"id": hub_counter["id"], **hub.dict()}
    hubs.append(new)
    hub_counter["id"] += 1
    return new

@app.put("/hubs/{hub_id}", response_model=HubResponse, tags=["Hubs"])
def update_hub(hub_id: int, hub: Hub):
    """Update hub details"""
    for i, h in enumerate(hubs):
        if h["id"] == hub_id:
            hubs[i] = {"id": hub_id, **hub.dict()}
            return hubs[i]
    raise HTTPException(status_code=404, detail="Hub not found")

@app.delete("/hubs/{hub_id}", tags=["Hubs"])
def delete_hub(hub_id: int):
    """Delete a hub"""
    for i, h in enumerate(hubs):
        if h["id"] == hub_id:
            hubs.pop(i)
            return {"message": f"Hub {hub_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Hub not found")

# ---------- Hub Parcel Routes ----------
@app.get("/hubs/{hub_id}/parcels", response_model=List[HubParcelResponse], tags=["Hub Parcels"])
def get_parcels_at_hub(hub_id: int):
    """Get all parcels at a specific hub"""
    return [p for p in parcels_at_hub if p["hub_id"] == hub_id]

@app.post("/hubs/parcels", response_model=HubParcelResponse, status_code=201, tags=["Hub Parcels"])
def add_parcel_to_hub(parcel: HubParcel):
    """Register a parcel arriving at a hub"""
    new = {"id": parcel_counter["id"], **parcel.dict()}
    parcels_at_hub.append(new)
    parcel_counter["id"] += 1
    return new

@app.patch("/hubs/parcels/{parcel_id}/status", response_model=HubParcelResponse, tags=["Hub Parcels"])
def update_parcel_status(parcel_id: int, status: str):
    """Update parcel status at hub (RECEIVED, SORTED, DISPATCHED)"""
    valid_statuses = ["RECEIVED", "SORTED", "DISPATCHED"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be: {valid_statuses}")
    for i, p in enumerate(parcels_at_hub):
        if p["id"] == parcel_id:
            parcels_at_hub[i]["status"] = status
            return parcels_at_hub[i]
    raise HTTPException(status_code=404, detail="Parcel not found")
