#!/bin/bash

echo "Creating database if it doesn't exist..."
python init_db.py

echo "Starting FastAPI dev server..."
uvicorn main:app --reload