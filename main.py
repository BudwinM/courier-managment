from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Tracking Service",
    description="Tracks parcel locations and delivery status in the Courier System",
    version="1.0.0"
)

# In-memory database
tracking_records = []
counter = {"id": 1}

# ---------- Models ----------
class TrackingRecord(BaseModel):
    order_id: int
    current_location: str
    status: str
    notes: Optional[str] = None
    timestamp: Optional[str] = None

class TrackingResponse(TrackingRecord):
    id: int

# ---------- Routes ----------
@app.get("/", tags=["Health"])
def root():
    return {"service": "Tracking Service", "status": "running"}

@app.get("/tracking", response_model=List[TrackingResponse], tags=["Tracking"])
def get_all_records():
    """Get all tracking records"""
    return tracking_records

@app.get("/tracking/{tracking_id}", response_model=TrackingResponse, tags=["Tracking"])
def get_tracking(tracking_id: int):
    """Get a tracking record by ID"""
    for t in tracking_records:
        if t["id"] == tracking_id:
            return t
    raise HTTPException(status_code=404, detail="Tracking record not found")

@app.get("/tracking/order/{order_id}", response_model=List[TrackingResponse], tags=["Tracking"])
def get_tracking_by_order(order_id: int):
    """Get full tracking history for a specific order"""
    history = [t for t in tracking_records if t["order_id"] == order_id]
    if not history:
        raise HTTPException(status_code=404, detail="No tracking records found for this order")
    return history

@app.post("/tracking", response_model=TrackingResponse, status_code=201, tags=["Tracking"])
def create_tracking(record: TrackingRecord):
    """Add a new tracking update for an order"""
    new = {
        "id": counter["id"],
        **record.dict(),
        "timestamp": record.timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tracking_records.append(new)
    counter["id"] += 1
    return new

@app.put("/tracking/{tracking_id}", response_model=TrackingResponse, tags=["Tracking"])
def update_tracking(tracking_id: int, record: TrackingRecord):
    """Update a tracking record"""
    for i, t in enumerate(tracking_records):
        if t["id"] == tracking_id:
            tracking_records[i] = {"id": tracking_id, **record.dict()}
            return tracking_records[i]
    raise HTTPException(status_code=404, detail="Tracking record not found")

@app.delete("/tracking/{tracking_id}", tags=["Tracking"])
def delete_tracking(tracking_id: int):
    """Delete a tracking record"""
    for i, t in enumerate(tracking_records):
        if t["id"] == tracking_id:
            tracking_records.pop(i)
            return {"message": f"Tracking record {tracking_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Tracking record not found")
