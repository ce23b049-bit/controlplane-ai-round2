# ControlPlane.ai — Enterprise AI Governance Gateway

ControlPlane.ai is a real-time governance, FinOps, and safety layer designed to evaluate Generative AI outputs and intercept risks before they reach end users. Built for multi-use-case enterprise environments, it balances latency budgets and risk tolerances across customer-facing and internal AI applications.

---

## Key Features

* **Multi-Use-Case Governance**: Enforces dynamic policies calibrated to specific application contexts, such as strict controls for customer support chatbots and flexible policies for internal copilots.
* **Tiered Action Logic**: Uses confidence scoring to determine the optimal response (ALLOW, EDIT, FLAG for human review, or BLOCK) to mitigate alert fatigue while managing organizational liability.
* **Inline PII Masking & Injection Defense**: Detects sensitive entities (e.g., SSNs) and applies token masking mid-stream while blocking high-confidence prompt injections.
* **Sub-5ms Latency Overhead**: Runs lightweight, out-of-band proxy checks to inspect streaming responses without degrading user experience.
* **Real-Time Audit Trail & Dashboard**: Logs structured event telemetry—including confidence scores, latency metrics, and enforcement triggers—for compliance oversight.

---

## Risk Containment Matrix

| Decision Tier | Trigger Condition | Action Taken |
| :--- | :--- | :--- |
| **ALLOW** | Risk score below threshold | Passes output directly to user |
| **EDIT** | PII / Sensitive entity detected | Masks entity inline (e.g., `[REDACTED_SSN]`) before rendering |
| **FLAG** | Ambiguous risk score | Escalates event to audit log for human review without breaking stream |
| **BLOCK** | High-confidence policy violation | Drops connection immediately with a safety error response |

---

## Project Structure

```text
controlplane-mvp/
├── security_engine.py   # Policy configuration, risk confidence scoring, & PII regex engine
├── gateway.py           # FastAPI dynamic proxy handling /v1/chat/{use_case} SSE streaming
├── dashboard.py         # Streamlit real-time governance HUD & event audit log
├── README.md            # Technical documentation
└── requirements.txt     # Python dependencies
Quickstart Guide
Prerequisites
Python 3.9 or higher

pip package manager

1. Installation
Clone the repository, create a virtual environment, and install dependencies:
git clone [https://github.com/ce23b049-bit/controlplane-ai-round2.git](https://github.com/ce23b049-bit/controlplane-ai-round2.git)
cd controlplane-mvp
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

pip install fastapi uvicorn httpx streamlit pandas

2. Run the Gateway Server
Start the FastAPI out-of-band proxy:

Bash
uvicorn gateway:app --reload --port 8000
Interactive API documentation is available at http://127.0.0.1:8000/docs.

3. Run the Live Dashboard
In a secondary terminal window (with the virtual environment activated), start the Streamlit HUD:

Bash
streamlit run dashboard.py
Access the live metrics and audit dashboard at http://localhost:8501.

API Usage Example
Send a POST request to test dynamic routing for different use cases:

Bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/v1/chat/customer_support](http://127.0.0.1:8000/v1/chat/customer_support)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {
      "role": "user",
      "content": "My social security number is 123-45-6789."
    }
  ]
}'
