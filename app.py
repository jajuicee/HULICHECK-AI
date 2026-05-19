import streamlit as st
import pandas as pd
import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(page_title="HuliCheck", page_icon="🚓", layout="wide", initial_sidebar_state="expanded")

# ──────────────────────────────────────────────
# PREMIUM CSS — LIGHT THEME REDESIGN
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ═══════════ GLOBAL ═══════════ */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: #f8fafc;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(56, 189, 248, 0.1), transparent),
        radial-gradient(ellipse 60% 40% at 80% 60%, rgba(139, 92, 246, 0.05), transparent);
    color: #1e293b;
}

/* ═══════════ SIDEBAR ═══════════ */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 20px rgba(0,0,0,0.02) !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li {
    color: #475569 !important;
    font-size: 0.85rem !important;
    line-height: 1.7 !important;
}
section[data-testid="stSidebar"] label {
    color: #64748b !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    font-weight: 700 !important;
}

/* ═══════════ HEADINGS ═══════════ */
h1 {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 30%, #0ea5e9 60%, #0284c7 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    font-size: 2.4rem !important;
}
section[data-testid="stSidebar"] h1 {
    font-size: 1.6rem !important;
    background: linear-gradient(135deg, #2563eb, #8b5cf6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 0.3rem !important;
}

/* ═══════════ CHAT MESSAGES ═══════════ */
.stChatMessage {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 1.2rem 1.5rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02) !important;
    color: #334155 !important;
}

/* ═══════════ METRIC CARDS ═══════════ */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e0e7ff !important;
    border-radius: 20px !important;
    padding: 1.8rem 1.5rem !important;
    text-align: center !important;
    box-shadow: 0 10px 25px -5px rgba(59,130,246,0.08) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 35px -5px rgba(59,130,246,0.12) !important;
}
[data-testid="stMetricValue"] {
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -1px !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    color: #64748b !important;
    font-weight: 700 !important;
}

/* ═══════════ CHAT INPUT ═══════════ */
[data-testid="stChatInput"] {
    border-radius: 16px !important;
}
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 14px !important;
    color: #1e293b !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03) !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
}

/* ═══════════ SELECTBOX ═══════════ */
.stSelectbox > div > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    color: #1e293b !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}

/* ═══════════ ALERTS ═══════════ */
.stAlert {
    border-radius: 14px !important;
    border: none !important;
}

/* ═══════════ CUSTOM COMPONENTS ═══════════ */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 1.2rem 0;
}

.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
.pill-purple {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
}
.pill-rose {
    background: #fdf2f8;
    color: #db2777;
    border: 1px solid #fbcfe8;
}

/* ═══════════ HERO / WELCOME ═══════════ */
.hero-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 2rem 2rem;
    animation: fadeInUp 0.8s ease-out;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.hero-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    filter: drop-shadow(0 10px 15px rgba(59,130,246,0.2));
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: #475569;
    max-width: 480px;
    line-height: 1.6;
    margin-bottom: 2rem;
}
.hero-chips {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    justify-content: center;
}
.hero-chip {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.7rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: #475569;
    cursor: default;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    transition: all 0.2s ease;
}
.hero-chip:hover {
    background: #f8fafc;
    border-color: #cbd5e1;
    color: #0f172a;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
}
.hero-chip span {
    margin-right: 6px;
}

/* ═══════════ RESULT CARDS ═══════════ */
.result-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #e2e8f0;
}
.result-header-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 0 4px rgba(16,185,129,0.2);
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.8; }
}
.result-header-text {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #64748b;
}

.conf-card {
    border-radius: 20px;
    padding: 1.2rem 0.8rem;
    text-align: center;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.conf-card:hover {
    transform: translateY(-2px);
}
.conf-danger {
    background: #fef2f2;
    border: 1px solid #fecaca;
}
.conf-danger:hover { box-shadow: 0 15px 35px -5px rgba(239,68,68,0.15); }
.conf-safe {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
}
.conf-safe:hover { box-shadow: 0 15px 35px -5px rgba(16,185,129,0.15); }
.conf-icon { font-size: 1.5rem; margin-bottom: 0.3rem; }
.conf-status {
    font-size: 1.1rem;
    font-weight: 800;
    margin: 0.2rem 0;
}
.conf-danger .conf-status { color: #dc2626; }
.conf-safe .conf-status { color: #059669; }
.conf-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 700;
}
.conf-danger .conf-label { color: #ef4444; }
.conf-safe .conf-label { color: #10b981; }

.script-card {
    background: #ffffff;
    border: 1px solid #e0e7ff;
    border-radius: 20px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    transition: transform 0.3s ease;
}
.script-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.05); }
.script-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #4f46e5;
    margin-bottom: 0.8rem;
}
.script-text {
    color: #334155;
    font-size: 1rem;
    line-height: 1.7;
    font-style: italic;
    font-weight: 500;
    margin: 0;
    padding-left: 1.2rem;
    border-left: 3px solid #c7d2fe;
}

/* ═══════════ SPINNER ═══════════ */
.stSpinner > div > div {
    border-top-color: #3b82f6 !important;
}

/* Make text inside chat messages readable in light theme */
.stChatMessage p {
    color: #334155 !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA LOADING (RAG micro-data)
# ──────────────────────────────────────────────
@st.cache_data
def load_violations():
    return pd.read_csv("violations.csv")

df = load_violations()

# ──────────────────────────────────────────────
# RENDER RESULT
# ──────────────────────────────────────────────
def render_result(parsed):
    # Header
    st.markdown("""
    <div class="result-header">
        <div class="result-header-dot"></div>
        <span class="result-header-text">Rights Assessment Complete</span>
    </div>
    """, unsafe_allow_html=True)

    fine_val = parsed.get('fine', 0)
    st.metric(label="Expected Fine", value=f"₱{fine_val:,}")

    # Helper for rendering penalty cards
    def penalty_card(title, is_true, icon_true, icon_false):
        if str(is_true).lower() == 'true' or is_true is True:
            return f'''
            <div class="conf-card conf-danger">
                <div class="conf-icon">{icon_true}</div>
                <div class="conf-status">YES</div>
                <div class="conf-label">{title}</div>
            </div>
            '''
        else:
            return f'''
            <div class="conf-card conf-safe">
                <div class="conf-icon">{icon_false}</div>
                <div class="conf-status">NO</div>
                <div class="conf-label">{title}</div>
            </div>
            '''

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(penalty_card("Confiscation", parsed.get('confiscation', False), "🚫", "✅"), unsafe_allow_html=True)
    with col2:
        st.markdown(penalty_card("Impound", parsed.get('impound', False), "🔒", "✅"), unsafe_allow_html=True)
    with col3:
        st.markdown(penalty_card("Jail Time", parsed.get('jail', False), "⚖️", "✅"), unsafe_allow_html=True)

    script = parsed.get('script', '')
    if script:
        st.markdown(f"""
        <div class="script-card">
            <div class="script-label">🗣️ Suggested Script for the Enforcer</div>
            <p class="script-text">"{script}"</p>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# AGENT TOOLS
# ──────────────────────────────────────────────
@tool
def violation_lookup(query: str) -> str:
    """Looks up traffic violations in the Philippine database. Provide a SINGLE short keyword like 'helmet', 'red light', 'license', 'alcohol', 'phone', 'unregistered', 'reckless'."""
    q = query.lower().strip()
    
    # Map common user terms to our CSV terminology
    synonyms = {
        "drunk": "alcohol",
        "intoxicated": "alcohol",
        "cellphone": "phone",
        "texting": "phone",
        "slippers": "shoe",
        "barefoot": "shoe",
        "no or/cr": "or/cr",
        "speeding": "reckless",
        "no seatbelt": "seatbelt",
        "seatbelt": "seatbelt",
    }
    q = synonyms.get(q, q)

    matches = []
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        if q in str(row_dict.get('Violation', '')).lower() or q in str(row_dict.get('Description', '')).lower():
            matches.append({
                "violation": row_dict.get('Violation', 'Unknown'),
                "fine": int(row_dict.get('Fine_Amount', 0)),
                "max_fine": int(row_dict.get('Max_Fine', row_dict.get('Fine_Amount', 0))),
                "confiscation": str(row_dict.get('License_Confiscation', 'False')).strip() == 'True',
                "impound": str(row_dict.get('Impound', 'False')).strip() == 'True',
                "jail": str(row_dict.get('Jail', 'False')).strip() == 'True',
            })
            
    if matches:
        return json.dumps(matches)
    return json.dumps({"error": f"No violation found for keyword '{query}'. Try a different single word."})

@tool
def fine_calculator(fine_amount: int, multiplier: int = 1) -> str:
    """Calculates total fine. Use multiplier for repeat offenses."""
    return json.dumps({"base_fine": fine_amount, "multiplier": multiplier, "total_fine": fine_amount * multiplier})

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🚓 HuliCheck")
    st.markdown("""
    <div style="display:flex; gap:8px; margin-bottom:0.5rem;">
        <span class="pill pill-purple">⚡ RAG</span>
        <span class="pill pill-rose">🤖 Agentic AI</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    vehicle_type = st.selectbox("VEHICLE TYPE", ["Motorcycle", "Private Car", "Public Utility Vehicle"])
    location = st.selectbox("LOCATION", ["Metro Manila (MMDA)", "LTO National", "Provincial"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
**How it works:**
1. Describe your traffic stop situation
2. Our RAG system retrieves exact violation data
3. The AI agent evaluates your rights
4. Receive your fine + what to say
    """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.caption("Powered by GPT-4o · Micro-data RAG · LangGraph Agent")

# ──────────────────────────────────────────────
# MAIN AREA
# ──────────────────────────────────────────────
st.title("🚓 HuliCheck")
st.caption("AI-Powered Traffic Apprehension Assistant for Philippine Drivers")

# ──────────────────────────────────────────────
# CHAT STATE
# ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show hero when no messages
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icon">🛡️</div>
        <div class="hero-title">Know Your Rights on the Road</div>
        <div class="hero-subtitle">
            Got pulled over? Describe your situation below and get an instant assessment — 
            exact fines, confiscation risk, and a polite script to protect your rights.
        </div>
        <div class="hero-chips">
            <div class="hero-chip"><span>🏍️</span> No Helmet</div>
            <div class="hero-chip"><span>🚦</span> Beating the Red Light</div>
            <div class="hero-chip"><span>🅿️</span> Illegal Parking</div>
            <div class="hero-chip"><span>🪪</span> No License</div>
            <div class="hero-chip"><span>🔄</span> Counterflow</div>
            <div class="hero-chip"><span>📅</span> Number Coding</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(msg["content"])
        else:
            if "parsed" in msg:
                render_result(msg["parsed"])
            else:
                st.markdown(msg["content"])

# ──────────────────────────────────────────────
# CHAT INPUT & AGENT
# ──────────────────────────────────────────────
if prompt := st.chat_input("Tell me what happened — e.g. 'I got stopped for no helmet'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your situation..."):
            try:
                OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "")
                if not OPENAI_KEY:
                    st.error("❌ OpenAI API key not found. Please add it to Streamlit secrets.")
                    st.stop()
                llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_KEY, temperature=0)
                tools = [violation_lookup, fine_calculator]

                sys_prompt = f"""You are a Rights Defender Agent for Philippine traffic law.
Context: User drives a {vehicle_type} in {location}.
INSTRUCTIONS:
1. Identify ALL distinct potential violations in the user's story (e.g. driving drunk, using phone, unregistered).
2. For EACH violation identified, call the violation_lookup tool with a SINGLE short keyword (e.g. 'alcohol' for drunk, 'phone' for cellphone, 'unregistered' for no registration).
3. Determine if the user mentions it is a repeat offense (e.g., "second time", "third time"). If it is a major repeat offense, use the 'max_fine' from the tool output; otherwise use 'fine'.
4. Calculate the TOTAL fine by adding them all up.
5. Set 'confiscation', 'impound', and 'jail' to true if ANY of the identified violations require them.
6. If you cannot find a fine, assume it is 0.
7. Return your FINAL answer as ONLY a JSON object (no markdown formatting, no backticks, no extra text):
{{"fine": <total_int>, "confiscation": <bool>, "impound": <bool>, "jail": <bool>, "script": "<1-2 sentence polite script acknowledging the specific violations and consequences>"}}"""

                agent = create_react_agent(llm, tools, prompt=sys_prompt)
                result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
                final_msg = result["messages"][-1].content
                clean_str = final_msg.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(clean_str)

                render_result(parsed)
                st.session_state.messages.append({"role": "assistant", "content": "", "parsed": parsed})

            except json.JSONDecodeError:
                st.error("⚠️ Could not parse agent response.")
                st.code(final_msg if 'final_msg' in dir() else "No output")
                st.session_state.messages.append({"role": "assistant", "content": f"Parse error"})
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
