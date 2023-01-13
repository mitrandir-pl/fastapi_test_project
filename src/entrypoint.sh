#!/bin/sh

sleep 5 && poetry run uvicorn main:app --reload --host 0.0.0.0
