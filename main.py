from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Billing Service",
    description="Manages invoices and payments in the Courier System",
    version="1.0.0"
)

# In-memory database
invoices = []
counter = {"id": 1}

# ---------- Models ----------
class Invoice(BaseModel):
    order_id: int
    customer_id: int
    amount: float
    description: str
    payment_status: Optional[str] = "UNPAID"  # UNPAID, PAID, CANCELLED
    created_at: Optional[str] = None

class InvoiceResponse(Invoice):
    id: int

# ---------- Routes ----------
@app.get("/", tags=["Health"])
def root():
    return {"service": "Billing Service", "status": "running"}

@app.get("/billing", response_model=List[InvoiceResponse], tags=["Billing"])
def get_all_invoices():
    """Get all invoices"""
    return invoices

@app.get("/billing/{invoice_id}", response_model=InvoiceResponse, tags=["Billing"])
def get_invoice(invoice_id: int):
    """Get an invoice by ID"""
    for inv in invoices:
        if inv["id"] == invoice_id:
            return inv
    raise HTTPException(status_code=404, detail="Invoice not found")

@app.get("/billing/customer/{customer_id}", response_model=List[InvoiceResponse], tags=["Billing"])
def get_invoices_by_customer(customer_id: int):
    """Get all invoices for a specific customer"""
    result = [inv for inv in invoices if inv["customer_id"] == customer_id]
    if not result:
        raise HTTPException(status_code=404, detail="No invoices found for this customer")
    return result

@app.get("/billing/order/{order_id}", response_model=List[InvoiceResponse], tags=["Billing"])
def get_invoices_by_order(order_id: int):
    """Get all invoices for a specific order"""
    return [inv for inv in invoices if inv["order_id"] == order_id]

@app.post("/billing", response_model=InvoiceResponse, status_code=201, tags=["Billing"])
def create_invoice(invoice: Invoice):
    """Create a new invoice"""
    new = {
        "id": counter["id"],
        **invoice.dict(),
        "created_at": invoice.created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    invoices.append(new)
    counter["id"] += 1
    return new

@app.put("/billing/{invoice_id}", response_model=InvoiceResponse, tags=["Billing"])
def update_invoice(invoice_id: int, invoice: Invoice):
    """Update an invoice"""
    for i, inv in enumerate(invoices):
        if inv["id"] == invoice_id:
            invoices[i] = {"id": invoice_id, **invoice.dict()}
            return invoices[i]
    raise HTTPException(status_code=404, detail="Invoice not found")

@app.patch("/billing/{invoice_id}/pay", response_model=InvoiceResponse, tags=["Billing"])
def mark_as_paid(invoice_id: int):
    """Mark an invoice as PAID"""
    for i, inv in enumerate(invoices):
        if inv["id"] == invoice_id:
            invoices[i]["payment_status"] = "PAID"
            return invoices[i]
    raise HTTPException(status_code=404, detail="Invoice not found")

@app.patch("/billing/{invoice_id}/cancel", response_model=InvoiceResponse, tags=["Billing"])
def cancel_invoice(invoice_id: int):
    """Cancel an invoice"""
    for i, inv in enumerate(invoices):
        if inv["id"] == invoice_id:
            invoices[i]["payment_status"] = "CANCELLED"
            return invoices[i]
    raise HTTPException(status_code=404, detail="Invoice not found")

@app.delete("/billing/{invoice_id}", tags=["Billing"])
def delete_invoice(invoice_id: int):
    """Delete an invoice"""
    for i, inv in enumerate(invoices):
        if inv["id"] == invoice_id:
            invoices.pop(i)
            return {"message": f"Invoice {invoice_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Invoice not found")
