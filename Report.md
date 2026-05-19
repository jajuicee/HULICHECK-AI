# Project Report: HuliCheck - AI-Powered Traffic Apprehension Assistant

## 1. Project Overview & Problem Statement
In the Philippines, encountering a traffic enforcer can be a stressful and confusing experience for motorists. Drivers are often unaware of the exact fines for specific violations, whether their license can legally be confiscated, or how to politely and effectively communicate with the enforcer. Misinformation and lack of accessible, on-the-spot legal guidance often lead to unnecessary disputes or unfair penalties.

**HuliCheck** was developed to solve this problem. It is a Python-based web application built on **Streamlit** that serves as an on-the-go "Rights Defender." By leveraging **Retrieval-Augmented Generation (RAG)** and **Agentic AI**, HuliCheck instantly evaluates a user’s traffic stop situation, retrieves the exact penalty data from a micro-database of MMDA/LTO rules, and provides a clear, factual assessment. 

## 2. Technical Architecture & Tech Stack
The application is designed to be lightweight, token-efficient, and easy to use. 

*   **Frontend (UI):** Streamlit. The interface is styled with a premium, responsive Light Theme using custom CSS. It features a sidebar for user context (vehicle type and location) and a dynamic chat interface (`st.chat_input` and `st.chat_message`) for interaction.
*   **Backend / AI Logic:** Python, LangChain, and LangGraph. The core intelligence is driven by OpenAI’s `gpt-4o` model.
*   **Database:** A localized CSV file (`violations.csv`) acting as a micro-database.

## 3. Core AI Concepts Implemented
HuliCheck successfully implements both required AI concepts: RAG and Agentic AI, tightly integrated to form a single cohesive workflow.

### A. Retrieval-Augmented Generation (RAG) via Micro-Data
Instead of using a heavy and expensive Vector Database (like Chroma or FAISS) to parse long, narrative legal documents, HuliCheck uses a **highly token-efficient micro-data approach**. 
Traffic laws are essentially structured facts. Our local database is a simple CSV containing explicit data points: Violation Name, Exact Fine Amount, and a Boolean flag for License Confiscation. 

When a user submits a query (e.g., "I got stopped for no helmet"), the system uses a custom tool to perform a lightweight Pandas keyword search against the CSV. It extracts only the exact matching row and injects a tiny JSON dictionary into the LLM’s context. This guarantees 100% factual accuracy (preventing LLM hallucinations regarding fine amounts) while keeping token usage to an absolute minimum.

### B. Agentic AI (LangGraph ReAct Agent)
The LLM does not merely answer questions; it operates as an autonomous agent using the **LangGraph** `create_react_agent` framework. 
The agent is equipped with specific tools:
1.  `violation_lookup`: To execute the RAG retrieval.
2.  `fine_calculator`: A logic tool to compute totals if repeat offenses are mentioned.

**The Agent Workflow:**
1.  **Observation:** The agent receives the user's natural language input along with their context (Vehicle Type and Location from the sidebar).
2.  **Action:** The agent autonomously decides to call the `violation_lookup` tool with an extracted keyword.
3.  **Synthesis:** After receiving the hard data from the tool, the agent evaluates the situation.
4.  **Structured Output:** To ensure UI reliability, the agent is strictly prompted to return its final answer as a JSON object containing the `fine` (int), `confiscation` (bool), and a `script` (a generated 1-2 sentence polite statement the driver can say to the enforcer).

The Streamlit frontend then parses this JSON and dynamically renders beautiful UI components (Metric Cards and Alert Boxes) rather than just printing a wall of text.

## 4. Conclusion and Future Work
HuliCheck demonstrates how Agentic AI and RAG can be combined to create a highly practical, real-world utility. By constraining the RAG retrieval to structured micro-data and forcing the Agent to output structured JSON, the application achieves a near-zero hallucination rate while remaining extremely cost-effective in terms of API tokens. 

Future iterations could expand the `violations.csv` to cover all municipal ordinances across the Philippines, integrate GPS for automatic location detection, and implement Voice-to-Text so drivers can speak to the app while keeping their hands on the wheel.
