# 🚓 HuliCheck

**AI-Powered Traffic Apprehension Assistant for Philippine Drivers**

HuliCheck is a Streamlit web application that helps Filipino drivers understand their rights during a traffic stop. Describe your situation in natural language and get an instant assessment of fines, license confiscation risk, vehicle impoundment, and jail time — plus a polite script to say to the enforcer.

## Features

- 🤖 **Agentic AI** — LangGraph ReAct agent with multi-step reasoning
- 📄 **RAG** — Token-efficient micro-data retrieval from a local CSV database
- 💬 **Chat Interface** — Natural language input via Streamlit chat
- ⚖️ **Multi-violation Detection** — Identifies and totals multiple violations in one query
- 🔁 **Repeat Offense Awareness** — Applies max fines for repeat offenders
- 🚗 **Consequence Cards** — Shows Confiscation, Impound, and Jail Time status

## Tech Stack

- Python, Streamlit
- LangChain, LangGraph (`create_react_agent`)
- OpenAI GPT-4o
- Pandas (CSV-based RAG)

## Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-openai-key-here"
   ```
4. Run locally:
   ```bash
   streamlit run app.py
   ```

## Deployment

Hosted on [Streamlit Community Cloud](https://share.streamlit.io). Add `OPENAI_API_KEY` under the app's **Secrets** settings before deploying.
