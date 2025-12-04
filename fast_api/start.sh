#!/bin/bash
# Start FastAPI server for LIP-SYNC-float-fast

# Activate virtual environment
source /home/psilab/LIP-SYNC-float-fast/venv/bin/activate

# Set working directory
cd /home/psilab/LIP-SYNC-float-fast

echo "Starting LIP-SYNC Float API..."
echo "API will be available at: http://localhost:8001"
echo "API docs available at: http://localhost:8001/docs"
echo ""

# Run the API
python fast_api/main.py
