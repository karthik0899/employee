#!/bin/bash

echo "Container is running!!!"



# Create venv if it does not exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Sync dependencies 
echo "Syncing dependencies..."
uv sync

echo "Environment ready! Virtual environment activated."
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"

# # Set database status for localhost development
# export DATABASE_STATUS='{"postgres-age-demo": {"active": true, "last_updated": "2025-06-20T12:00:00Z"}}'
# echo "Database status set for localhost development"

# Run the api/service.py file with the instantiated app FastAPI
uvicorn_server() {
    uvicorn apis.main_api:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir apis/ "$@"
}

uvicorn_server_production() {
    uv run uvicorn main:app --host 0.0.0.0 --port 9000 --lifespan on
}

export -f uvicorn_server
export -f uvicorn_server_production

echo -en "\033[92m
The following commands are available:
    uvicorn_server
        Run the Uvicorn Server
\033[0m
"

if [ "${DEV}" = 1 ]; then
    source .venv/bin/activate
    # Development mode: Keep shell open
    exec /bin/bash
else
    # Production mode: Run server in the foreground
    uvicorn_server_production
fi