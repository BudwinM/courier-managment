from flask import Flask, request, jsonify, Response
from flasgger import Swagger
import requests

app = Flask(__name__)

# ─── Service Registry ──────────────────────────────────────────────
SERVICES = {
    "billing":  "http://localhost:5001",
    "branch":   "http://localhost:5002",
    "orders":   "http://localhost:5003",
    "tracking": "http://localhost:5004",
    "delivery": "http://localhost:5005",
    "customer": "http://localhost:5006",
}

# ─── Unified Swagger (shows all microservice endpoints) ───────────
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Online Courier Management — API Gateway",
        "description": (
            "Unified API Gateway for the Online Courier Management System.\n\n"
            "All microservice endpoints are accessible through this single gateway on **port 5000**.\n\n"
            "| Service | Developer | Direct Port | Gateway Prefix |\n"
            "|---------|-----------|-------------|----------------|\n"
            "| Billing API | Minidu | 5001 | /billing |\n"
            "| Branch API | Tharaka | 5002 | /branch |\n"
            "| Orders API | Budwin | 5003 | /orders |\n"
            "| Tracking API | Thisath | 5004 | /tracking |\n"
            "| Delivery API | Vihanga | 5005 | /delivery |\n"
            "| Customer API | Navoda | 5006 | /customer |"
        ),
        "version": "1.0.0"
    },
    "basePath": "/",
    "tags": [
        {"name": "Gateway",  "description": "API Gateway health & service registry"},
        {"name": "Billing",  "description": "Invoice & payment management — Minidu"},
        {"name": "Branch",   "description": "Branch management — Tharaka"},
        {"name": "Orders",   "description": "Courier order management — Budwin"},
        {"name": "Tracking", "description": "Package tracking — Thisath"},
        {"name": "Delivery", "description": "Delivery & rider management — Vihanga"},
        {"name": "Customer", "description": "Customer management — Navoda"},
    ],
    "paths": {
        # ── Gateway ──────────────────────────────────────────────────
        "/health": {
            "get": {
                "tags": ["Gateway"],
                "summary": "Gateway health check",
                "responses": {"200": {"description": "Gateway is healthy"}}
            }
        },
        "/services": {
            "get": {
                "tags": ["Gateway"],
                "summary": "List all registered microservices",
                "responses": {"200": {"description": "Service registry"}}
            }
        },
        # ── Billing ──────────────────────────────────────────────────
        "/billing/invoices": {
            "get": {
                "tags": ["Billing"],
                "summary": "Get all invoices",
                "responses": {"200": {"description": "List of invoices"}}
            },
            "post": {
                "tags": ["Billing"],
                "summary": "Create a new invoice",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["order_id", "customer_name", "amount", "currency"],
                        "properties": {
                            "order_id":       {"type": "string",  "example": "ORD-001"},
                            "customer_name":  {"type": "string",  "example": "John Doe"},
                            "amount":         {"type": "number",  "example": 1500.00},
                            "currency":       {"type": "string",  "example": "LKR"},
                            "description":    {"type": "string",  "example": "Courier charge"}
                        }
                    }
                }],
                "responses": {"201": {"description": "Invoice created"}}
            }
        },
        "/billing/invoices/{invoice_id}": {
            "get": {
                "tags": ["Billing"],
                "summary": "Get invoice by ID",
                "parameters": [{"name": "invoice_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Invoice found"}, "404": {"description": "Not found"}}
            },
            "delete": {
                "tags": ["Billing"],
                "summary": "Delete an invoice",
                "parameters": [{"name": "invoice_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Deleted"}}
            }
        },
        "/billing/invoices/{invoice_id}/pay": {
            "put": {
                "tags": ["Billing"],
                "summary": "Mark invoice as paid",
                "parameters": [
                    {"name": "invoice_id", "in": "path", "required": True, "type": "string"},
                    {
                        "name": "body", "in": "body", "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["payment_method"],
                            "properties": {
                                "payment_method": {"type": "string", "example": "CARD"},
                                "transaction_id":  {"type": "string", "example": "TXN-98765"}
                            }
                        }
                    }
                ],
                "responses": {"200": {"description": "Invoice paid"}}
            }
        },
        # ── Branch ───────────────────────────────────────────────────
        "/branch/branches": {
            "get": {
                "tags": ["Branch"],
                "summary": "Get all branches",
                "responses": {"200": {"description": "List of branches"}}
            },
            "post": {
                "tags": ["Branch"],
                "summary": "Create a new branch",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["name", "city", "address", "contact_number"],
                        "properties": {
                            "name":           {"type": "string", "example": "Colombo Central"},
                            "city":           {"type": "string", "example": "Colombo"},
                            "address":        {"type": "string", "example": "123 Main St"},
                            "contact_number": {"type": "string", "example": "+94112345678"},
                            "manager_name":   {"type": "string", "example": "Tharaka Perera"}
                        }
                    }
                }],
                "responses": {"201": {"description": "Branch created"}}
            }
        },
        "/branch/branches/{branch_id}": {
            "get": {
                "tags": ["Branch"],
                "summary": "Get branch by ID",
                "parameters": [{"name": "branch_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Branch found"}}
            },
            "put": {
                "tags": ["Branch"],
                "summary": "Update a branch",
                "parameters": [
                    {"name": "branch_id", "in": "path", "required": True, "type": "string"},
                    {
                        "name": "body", "in": "body", "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name":           {"type": "string"},
                                "city":           {"type": "string"},
                                "address":        {"type": "string"},
                                "contact_number": {"type": "string"},
                                "manager_name":   {"type": "string"},
                                "status":         {"type": "string", "example": "ACTIVE"}
                            }
                        }
                    }
                ],
                "responses": {"200": {"description": "Branch updated"}}
            },
            "delete": {
                "tags": ["Branch"],
                "summary": "Delete a branch",
                "parameters": [{"name": "branch_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Deleted"}}
            }
        },
        # ── Orders ───────────────────────────────────────────────────
        "/orders/orders": {
            "get": {
                "tags": ["Orders"],
                "summary": "Get all orders",
                "responses": {"200": {"description": "List of orders"}}
            },
            "post": {
                "tags": ["Orders"],
                "summary": "Create a new courier order",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["sender_name", "sender_address", "receiver_name", "receiver_address", "package_weight_kg", "branch_id"],
                        "properties": {
                            "sender_name":       {"type": "string",  "example": "Budwin Fernando"},
                            "sender_address":    {"type": "string",  "example": "12 Galle Rd, Colombo"},
                            "receiver_name":     {"type": "string",  "example": "Amal Perera"},
                            "receiver_address":  {"type": "string",  "example": "45 Kandy Rd, Kandy"},
                            "package_weight_kg": {"type": "number",  "example": 2.5},
                            "package_type":      {"type": "string",  "example": "FRAGILE"},
                            "branch_id":         {"type": "string",  "example": "BR-ABC12345"},
                            "special_instructions": {"type": "string", "example": "Handle with care"}
                        }
                    }
                }],
                "responses": {"201": {"description": "Order created"}}
            }
        },
        "/orders/orders/{order_id}": {
            "get": {
                "tags": ["Orders"],
                "summary": "Get order by ID",
                "parameters": [{"name": "order_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Order found"}}
            },
            "delete": {
                "tags": ["Orders"],
                "summary": "Cancel an order",
                "parameters": [{"name": "order_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Cancelled"}}
            }
        },
        "/orders/orders/{order_id}/status": {
            "put": {
                "tags": ["Orders"],
                "summary": "Update order status",
                "parameters": [
                    {"name": "order_id", "in": "path", "required": True, "type": "string"},
                    {
                        "name": "body", "in": "body", "required": True,
                        "schema": {
                            "type": "object",
                            "required": ["status"],
                            "properties": {
                                "status": {"type": "string", "enum": ["PENDING", "CONFIRMED", "IN_TRANSIT", "DELIVERED", "CANCELLED"], "example": "CONFIRMED"}
                            }
                        }
                    }
                ],
                "responses": {"200": {"description": "Status updated"}}
            }
        },
        # ── Tracking ─────────────────────────────────────────────────
        "/tracking/tracking": {
            "get": {
                "tags": ["Tracking"],
                "summary": "Get all tracking records",
                "responses": {"200": {"description": "All tracking records"}}
            },
            "post": {
                "tags": ["Tracking"],
                "summary": "Create a tracking record",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["order_id", "current_location", "status"],
                        "properties": {
                            "order_id":         {"type": "string", "example": "ORD-ABC12345"},
                            "current_location": {"type": "string", "example": "Colombo Sorting Center"},
                            "status":           {"type": "string", "enum": ["PICKED_UP", "IN_TRANSIT", "AT_HUB", "OUT_FOR_DELIVERY", "DELIVERED"], "example": "PICKED_UP"},
                            "notes":            {"type": "string", "example": "Picked up from sender"},
                            "latitude":         {"type": "number", "example": 6.9271},
                            "longitude":        {"type": "number", "example": 79.8612}
                        }
                    }
                }],
                "responses": {"201": {"description": "Tracking record created"}}
            }
        },
        "/tracking/tracking/{tracking_id}": {
            "get": {
                "tags": ["Tracking"],
                "summary": "Get tracking by ID",
                "parameters": [{"name": "tracking_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Tracking found"}}
            },
            "put": {
                "tags": ["Tracking"],
                "summary": "Update tracking location/status",
                "parameters": [
                    {"name": "tracking_id", "in": "path", "required": True, "type": "string"},
                    {
                        "name": "body", "in": "body", "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "current_location": {"type": "string", "example": "Kandy Hub"},
                                "status":           {"type": "string", "example": "AT_HUB"},
                                "notes":            {"type": "string"},
                                "latitude":         {"type": "number"},
                                "longitude":        {"type": "number"}
                            }
                        }
                    }
                ],
                "responses": {"200": {"description": "Updated"}}
            },
            "delete": {
                "tags": ["Tracking"],
                "summary": "Delete tracking record",
                "parameters": [{"name": "tracking_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Deleted"}}
            }
        },
        "/tracking/tracking/order/{order_id}": {
            "get": {
                "tags": ["Tracking"],
                "summary": "Get tracking records by Order ID",
                "parameters": [{"name": "order_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Tracking records for order"}}
            }
        },
        # ── Delivery ─────────────────────────────────────────────────
        "/delivery/deliveries": {
            "get": {
                "tags": ["Delivery"],
                "summary": "Get all deliveries",
                "responses": {"200": {"description": "List of deliveries"}}
            },
            "post": {
                "tags": ["Delivery"],
                "summary": "Create a delivery assignment",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["order_id", "rider_id", "pickup_address", "delivery_address"],
                        "properties": {
                            "order_id":                {"type": "string", "example": "ORD-ABC12345"},
                            "rider_id":                {"type": "string", "example": "RDR-XYZ98765"},
                            "pickup_address":          {"type": "string", "example": "Colombo Sorting Center"},
                            "delivery_address":        {"type": "string", "example": "45 Temple Road, Kandy"},
                            "estimated_delivery_date": {"type": "string", "example": "2026-04-05"},
                            "priority":                {"type": "string", "enum": ["STANDARD", "EXPRESS", "SAME_DAY"], "example": "EXPRESS"}
                        }
                    }
                }],
                "responses": {"201": {"description": "Delivery created"}}
            }
        },
        "/delivery/deliveries/{delivery_id}": {
            "get": {
                "tags": ["Delivery"],
                "summary": "Get delivery by ID",
                "parameters": [{"name": "delivery_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Delivery found"}}
            },
            "delete": {
                "tags": ["Delivery"],
                "summary": "Cancel a delivery",
                "parameters": [{"name": "delivery_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Cancelled"}}
            }
        },
        "/delivery/deliveries/{delivery_id}/complete": {
            "put": {
                "tags": ["Delivery"],
                "summary": "Mark delivery as completed",
                "parameters": [
                    {"name": "delivery_id", "in": "path", "required": True, "type": "string"},
                    {
                        "name": "body", "in": "body", "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "recipient_signature": {"type": "string", "example": "Amal Perera"},
                                "delivery_notes":      {"type": "string", "example": "Left with neighbour"}
                            }
                        }
                    }
                ],
                "responses": {"200": {"description": "Delivery completed"}}
            }
        },
        "/delivery/riders": {
            "get": {
                "tags": ["Delivery"],
                "summary": "Get all riders",
                "responses": {"200": {"description": "List of riders"}}
            },
            "post": {
                "tags": ["Delivery"],
                "summary": "Register a new rider",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["name", "phone", "vehicle_type", "branch_id"],
                        "properties": {
                            "name":           {"type": "string", "example": "Vihanga Dissanayake"},
                            "phone":          {"type": "string", "example": "+94771234567"},
                            "vehicle_type":   {"type": "string", "enum": ["MOTORCYCLE", "VAN", "TRUCK"], "example": "MOTORCYCLE"},
                            "branch_id":      {"type": "string", "example": "BR-ABC12345"},
                            "license_number": {"type": "string", "example": "LK-1234567"}
                        }
                    }
                }],
                "responses": {"201": {"description": "Rider registered"}}
            }
        },
        # ── Customer ─────────────────────────────────────────────────
        "/customer/customers": {
            "get": {
                "tags": ["Customer"],
                "summary": "Get all customers",
                "responses": {"200": {"description": "List of customers"}}
            },
            "post": {
                "tags": ["Customer"],
                "summary": "Create a new customer",
                "parameters": [{
                    "name": "body", "in": "body", "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["name", "email", "phone", "address"],
                        "properties": {
                            "name":    {"type": "string", "example": "Jane Doe"},
                            "email":   {"type": "string", "example": "jane@example.com"},
                            "phone":   {"type": "string", "example": "+94771234567"},
                            "address": {"type": "string", "example": "123 Main St, Colombo"}
                        }
                    }
                }],
                "responses": {"201": {"description": "Customer created"}}
            }
        },
        "/customer/customers/{customer_id}": {
            "get": {
                "tags": ["Customer"],
                "summary": "Get customer by ID",
                "parameters": [{"name": "customer_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Customer found"}, "404": {"description": "Customer not found"}}
            },
            "put": {
                "tags": ["Customer"],
                "summary": "Update customer details",
                "parameters": [
                    {"name": "customer_id", "in": "path", "required": True, "type": "string"},
                    {
                        "name": "body", "in": "body", "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name":    {"type": "string"},
                                "email":   {"type": "string"},
                                "phone":   {"type": "string"},
                                "address": {"type": "string"},
                                "status":  {"type": "string", "example": "INACTIVE"}
                            }
                        }
                    }
                ],
                "responses": {"200": {"description": "Customer updated"}}
            },
            "delete": {
                "tags": ["Customer"],
                "summary": "Delete a customer",
                "parameters": [{"name": "customer_id", "in": "path", "required": True, "type": "string"}],
                "responses": {"200": {"description": "Customer deleted"}}
            }
        },
    }
}

swagger = Swagger(app, template=swagger_template, config={
    "hide_top_bar": True,
    "footer_text": "<style>.swagger-ui .wrapper .clear { display: none !important; }</style>",
    "headers": [],
    "specs": [{"endpoint": "apispec", "route": "/apispec.json"}],
    "swagger_ui": True,
    "specs_route": "/swagger/",
})


# ─── Gateway own endpoints ─────────────────────────────────────────

@app.route("/health", methods=["GET"])
def gateway_health():
    """Gateway health check (not proxied to swagger above — handled directly)"""
    return jsonify({
        "service": "api-gateway",
        "status": "healthy",
        "port": 5000,
        "registered_services": list(SERVICES.keys())
    }), 200


@app.route("/services", methods=["GET"])
def list_services():
    """List all registered microservices"""
    return jsonify({
        name: {
            "url": url,
            "swagger": f"{url}/swagger/",
            "health": f"{url}/health"
        }
        for name, url in SERVICES.items()
    }), 200


# ─── Proxy helper ──────────────────────────────────────────────────

def proxy(service_name, path):
    base = SERVICES.get(service_name)
    if not base:
        return jsonify({"error": f"Service '{service_name}' not found"}), 404
    url = f"{base}/{path}"
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k.lower() != "host"},
            data=request.get_data(),
            params=request.args,
            timeout=10
        )
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type", "application/json"))
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Service '{service_name}' is unavailable. Make sure it is running on {base}"}), 503


# ─── Proxy routes ──────────────────────────────────────────────────

@app.route("/billing/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def billing_proxy(path):
    return proxy("billing", path)

@app.route("/branch/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def branch_proxy(path):
    return proxy("branch", path)

@app.route("/orders/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def orders_proxy(path):
    return proxy("orders", path)

@app.route("/tracking/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def tracking_proxy(path):
    return proxy("tracking", path)

@app.route("/delivery/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def delivery_proxy(path):
    return proxy("delivery", path)

@app.route("/customer/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def customer_proxy(path):
    return proxy("customer", path)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Online Courier Management — API Gateway")
    print("  Running on http://localhost:5000")
    print("  Swagger UI: http://localhost:5000/swagger/")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
