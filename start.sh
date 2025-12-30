#!/bin/bash

# Kill any existing processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:4321 | xargs kill -9 2>/dev/null

echo "🚀 Starting Flacon-Cloud Demo..."

# Start Backend
echo "🌸 Starting Backend (FastAPI)..."
cd backend
# Use the virtual environment python
./venv/bin/python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "✨ Starting Frontend (Astro)..."
npm run dev -- --port 4321 &
FRONTEND_PID=$!

echo "✅ System is running!"
echo "👉 Store: http://localhost:4321"
echo "👉 Admin: http://localhost:4321/admin"
echo "👉 API:   http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop everything"

# Wait for both processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
