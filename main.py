from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Customer Service",
    description="Manages customers in the Courier System",
    version="1.0.0"
)

# In-memory database
customers = []
counter = {"id": 1}

# ---------- Models ----------
class Customer(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class CustomerResponse(Customer):
    id: int

# ---------- Routes ----------
@app.get("/", tags=["Health"])
def root():
    return {"service": "Customer Service", "status": "running"}

@app.get("/customers", response_model=List[CustomerResponse], tags=["Customers"])
def get_all_customers():
    """Get all customers"""
    return customers

@app.get("/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
def get_customer(customer_id: int):
    """Get a customer by ID"""
    for c in customers:
        if c["id"] == customer_id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/customers", response_model=CustomerResponse, status_code=201, tags=["Customers"])
def create_customer(customer: Customer):
    """Create a new customer"""
    new = {"id": counter["id"], **customer.dict()}
    customers.append(new)
    counter["id"] += 1
    return new

@app.put("/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
def update_customer(customer_id: int, customer: Customer):
    """Update an existing customer"""
    for i, c in enumerate(customers):
        if c["id"] == customer_id:
            customers[i] = {"id": customer_id, **customer.dict()}
            return customers[i]
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}", tags=["Customers"])
def delete_customer(customer_id: int):
    """Delete a customer"""
    for i, c in enumerate(customers):
        if c["id"] == customer_id:
            customers.pop(i)
            return {"message": f"Customer {customer_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")
