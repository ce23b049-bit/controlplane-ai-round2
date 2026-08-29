import streamlit as st
import pandas as pd

st.set_page_config(page_title="ControlPlane.ai HUD", layout="wide")
st.title("ControlPlane.ai — Live Governance HUD")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Proxy Latency", "< 3.8 ms", "-99% vs LLM-Judge")
c2.metric("API Cost / 1k Requests", "$23.00", "-39.4% Savings")
c3.metric("Live Interceptions", "1,240", "100% Pre-render")
c4.metric("False Positive Rate", "1.2%", "Monitoring")

st.subheader("Real-Time Event Audit Log")
st.json([
    {"use_case": "customer_support", "time": "15:01:02", "type": "PII Masked", "target": "SSN", "latency": "1.1ms", "action": "EDIT", "confidence": 0.85},
    {"use_case": "internal_copilot", "time": "15:00:44", "type": "Prompt Injection", "target": "Jailbreak", "latency": "2.1ms", "action": "BLOCK", "confidence": 0.95}
])