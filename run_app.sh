#!/bin/bash
# Launch script for Background Remover Streamlit App

cd "$(dirname "$0")"
.venv/bin/streamlit run app.py
