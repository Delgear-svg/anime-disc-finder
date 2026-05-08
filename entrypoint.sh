#!/bin/bash
# Start cron daemon and Streamlit
cron
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
