# 📦 Online Courier Management System — Microservices Backend

Welcome to our project repository! 👋 

This is the backend for our **Online Courier Management System**, developed as part of our **IT4020 Modern Topics in IT — Assignment 2** at the **Sri Lanka Institute of Information Technology (SLIIT)**. 🎓

We've designed a modern, robust, and scalable microservices architecture to handle all the moving parts of a real-world courier service. Everything is tied together with a unifying API Gateway!

---

## 👨‍💻 Meet the Team & Our Microservices

Our system is divided into functional microservices, each carefully crafted by a team member. Here's exactly who built what:

- **Minidu** 💳 built the **Billing API** (`Port 5001`) — Handles all invoices and payments. [Swagger Docs](http://localhost:5001/swagger/)
- **Tharaka** 🏢 engineered the **Branch API** (`Port 5002`) — Manages all our courier branches. [Swagger Docs](http://localhost:5002/swagger/)
- **Budwin** 📦 brought the **Orders API** to life (`Port 5003`) — Takes care of order placement and management. [Swagger Docs](http://localhost:5003/swagger/)
- **Thisath** 📍 tracked down the **Tracking API** (`Port 5004`) — Keeps customers updated on their package location. [Swagger Docs](http://localhost:5004/swagger/)
- **Vihanga** 🚚 delivered the **Delivery API** (`Port 5005`) — Manages riders and delivery statuses. [Swagger Docs](http://localhost:5005/swagger/)
- **Navoda** 🤝 joined with the **Customer Service API** (`Port 5006`) — Handling all customer profiles and inquiries. [Swagger Docs](http://localhost:5006/swagger/)

*Wait, how does all this connect?* We use an **API Gateway** (`Port 5000`) functioning as the grand orchestrator to route all requests perfectly to their respective services! 🚦

---

## 🏗️ Project Structure

We've kept things organized and modular. Each service lives independently in its own cozy folder:

```text
courier-management/
├── api-gateway/            # 🚦 Unified API Gateway (Port 5000)
├── billing-service/        # 💳 Billing API (Port 5001)
├── branch-service/         # 🏢 Branch API (Port 5002)
├── orders-service/         # 📦 Orders API (Port 5003)
├── tracking-service/       # 📍 Tracking API (Port 5004)
├── delivery-service/       # 🚚 Delivery API (Port 5005)
├── customer-service/       # 🤝 Customer API (Port 5006)
├── requirements.txt        # 📚 Shared dependencies
├── start_all.sh            # 🚀 Start script (Mac/Linux)
├── start_all.bat           # 🚀 Start script (Windows)
└── README.md
```

---

## 🚀 Getting Started

Let's get this system running on your local machine! First, make sure you have **Python 3.8+** and `pip` installed.

### 1️⃣ Install Dependencies

Open your terminal in the main project folder and install the shared requirements. (It might be a good idea to set up a virtual environment, but that's up to you!)

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Services

**If you're using Mac/Linux:**
We wrote a handy script to fire up all the services at once. Just make it executable and run it:

```bash
chmod +x start_all.sh
./start_all.sh
```

**If you're using Windows:**
You can just double-click `start_all.bat`, or if you prefer the manual way, open a separate terminal for each service and run `python app.py` in each folder. Make sure the API Gateway is running on Port 5000!

```bash
# Example
cd billing-service && python app.py
```

---

## 🚦 How Our API Gateway Works

The API Gateway is the star of the show! It runs on **Port 5000** and intelligently routes your requests behind the scenes.

**Here's the routing table:**
```text
Client → Gateway (5000) → /billing/*   → Billing Service  (5001)
                        → /branch/*    → Branch Service   (5002)
                        → /orders/*    → Orders Service   (5003)
                        → /tracking/*  → Tracking Service (5004)
                        → /delivery/*  → Delivery Service (5005)
                        → /customers/* → Customer Service (5006)
```

**Why go through the trouble?**
- **Simplicity:** Clients only need to talk to `localhost:5000`.
- **Security:** We don't expose individual service ports strictly to external clients.
- **Centralization:** Perfect place to add our authentication and rate-limiting later on.

---

## 📚 API Endpoints Summary

Here's a quick cheat sheet for everything our APIs can do through the gateway. Dive into the Swagger UI of each service to test them out intuitively.

### 💳 Billing Service — Minidu
*Accessed via `5000/billing/...`*

- `GET    /billing/invoices` — View all invoices
- `POST   /billing/invoices` — Generate a new invoice
- `GET    /billing/invoices/{id}` — Grab details of a specific invoice
- `PUT    /billing/invoices/{id}/pay` — Cha-ching! Mark an invoice as paid
- `DELETE /billing/invoices/{id}` — Remove an invoice

### 🏢 Branch Service — Tharaka
*Accessed via `5000/branch/...`*

- `GET    /branches` — See all courier branches
- `POST   /branches` — Set up a new branch location
- `GET    /branches/{id}` — Check details of a single branch
- `PUT    /branches/{id}` — Update branch information
- `DELETE /branches/{id}` — Close down a branch

### 📦 Orders Service — Budwin
*Accessed via `5000/orders/...`*

- `GET    /orders` — List every order in the system
- `POST   /orders` — Someone wants to send a package! (Create order)
- `GET    /orders/{id}` — Inspect a specific order
- `PUT    /orders/{id}/status` — Move an order through its lifecycle
- `DELETE /orders/{id}` — Cancel an order

### 📍 Tracking Service — Thisath
*Accessed via `5000/tracking/...`*

- `GET    /tracking` — Get all live tracking records
- `POST   /tracking` — Start tracking a new movement
- `GET    /tracking/{id}` — Get a specific tracking update
- `GET    /tracking/order/{order_id}` — Find where an order is right now
- `PUT    /tracking/{id}` — Update the location or status of a package
- `DELETE /tracking/{id}` — Erase a tracking history

### 🚚 Delivery Service — Vihanga
*Accessed via `5000/delivery/...`*

- `GET    /deliveries` — Overview of all active deliveries
- `POST   /deliveries` — Dispatch a package with a rider
- `GET    /deliveries/{id}` — Check on a specific delivery's status
- `PUT    /deliveries/{id}/complete` — Package delivered successfully!
- `DELETE /deliveries/{id}` — Cancel an ongoing delivery
- `GET    /riders` — See all registered delivery riders
- `POST   /riders` — Welcome a new rider to the team

### 🤝 Customer Service — Navoda
*Accessed via `5000/customers/...`*

- `GET    /customers` — Get our entire customer base
- `POST   /customers` — Register a brand new customer
- `GET    /customers/{id}` — Look up an individual user profile
- `PUT    /customers/{id}` — Update their contact details
- `DELETE /customers/{id}` — Remove a customer from the system

---

## 📖 Swagger Documentation

We believe good code needs good documentation. That's why we've fully documented every single endpoint! 

You can try out any feature interactively by visiting the **Unified API Gateway Swagger UI**:
👉 **[http://localhost:5000/swagger/](http://localhost:5000/swagger/)**

If you want to look at a specific microservice natively, just navigate to their respective native port (e.g., `http://localhost:5001/swagger/`). Have fun exploring! 🎉
