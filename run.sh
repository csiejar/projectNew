#!/bin/bash
pip3 install -r ./backend/requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload