#!/bin/bash
# ================================================================
#  Online Courier Management System — Start All Services
# ================================================================

echo ""
echo "========================================================"
echo "  Online Courier Management — Microservices Startup"
echo "========================================================"

# Install dependencies (run once)
pip install -r requirements.txt -q

echo ""
echo "Starting microservices..."
echo ""

# Start each microservice in background
python billing-service/app.py &
echo "  [✓] Billing Service   → http://localhost:5001  (Minidu)"
echo "       Swagger          → http://localhost:5001/swagger/"

python branch-service/app.py &
echo "  [✓] Branch Service    → http://localhost:5002  (Tharaka)"
echo "       Swagger          → http://localhost:5002/swagger/"

python orders-service/app.py &
echo "  [✓] Orders Service    → http://localhost:5003  (Budwin)"
echo "       Swagger          → http://localhost:5003/swagger/"

python tracking-service/app.py &
echo "  [✓] Tracking Service  → http://localhost:5004  (Thisath)"
echo "       Swagger          → http://localhost:5004/swagger/"

python delivery-service/app.py &
echo "  [✓] Delivery Service  → http://localhost:5005  (Vihanga)"
echo "       Swagger          → http://localhost:5005/swagger/"

sleep 2

# Start API Gateway last
python api-gateway/app.py &
echo ""
echo "  [✓] API Gateway       → http://localhost:5000"
echo "       Unified Swagger  → http://localhost:5000/swagger/"
echo ""
echo "========================================================"
echo "  All services are running!"
echo "  Use Ctrl+C to stop all services"
echo "========================================================"
echo ""

wait
