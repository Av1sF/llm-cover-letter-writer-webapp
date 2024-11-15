#!/bin/sh
uvicorn model_server.server:app --port 8000 & flask --app app.app run &