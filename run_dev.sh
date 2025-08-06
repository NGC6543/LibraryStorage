#!/bin/bash

# cd app
echo "Creating database if it doesn't exist..."
python app\\init_db.py

echo "Starting FastAPI dev server..."
uvicorn app.main:app