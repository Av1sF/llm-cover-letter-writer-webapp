#!/bin/sh
uvicorn model_server.server:app --port 2000 & flask --app app.app run &