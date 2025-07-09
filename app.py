from env_config import load_environment
load_environment()

import streamlit as st
from pipeline.learning_pipeline import run_learning_session

# Streamlit App Config
st.set_page_config(page_title="📚 Multi-Agent Edu", layout="wide")

# Custom Styling
st.markdown("""
<style>
    body, .block-container {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    .glass-container {
        background: #f3f4f6;
        border-radius: 15px;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .agent-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 8px;
        color: #1f2937;
    }

    h1, h2, h3, h4, h5, h6, p, div {
        color: #111827;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
    }

    .stTextInput > div > div > input {
        background: #ffffff;
        color: #111827;
        border: 1px solid #d1d5db;
        padding: 12px;
        font-size: 16px;
        border-radius: 10px;
    }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 24px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
    }

    /* Lighten markdown code blocks */
    code, pre {
        background-color: #f3f4f6 !important;
        color: #111827 !important;
        border-radius: 8px;
        padding: 10px;
        font-size: 15px;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Layout
col_main, col_guide = st.columns([2, 1])

with col_main:
    st.markdown("<h1 style='text-align: center;'>📚 Multi-Agent Edu</h1>", unsafe_allow_html=True)
    topic = st.text_input("Enter a learning topic:", placeholder="e.g., Newton's Laws, Python Lists, Photosynthesis")

    if st.button("Start Learning Session"):
        if not topic.strip():
            st.warning("Please enter a valid topic to begin.")
        else:
            st.info("Agents are collaborating. Please wait...")
            results = run_learning_session(topic)

            for i, step in enumerate(results):
                st.markdown(f'<div class="glass-container"><div class="agent-title">👨‍🎓 Step {i+1} — Student\'s Question</div><div>{step["student_question"]}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="glass-container"><div class="agent-title">👨‍🏫 Teacher\'s Explanation</div><div>{step["teacher_response"]}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="glass-container"><div class="agent-title">🔁 Student\'s Follow-up</div><div>{step["student_follow_up"]}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="glass-container"><div class="agent-title">🧪 Validator\'s Feedback</div><div>{step["validator_feedback"]}</div></div>', unsafe_allow_html=True)

with col_guide:
    st.header("🧭 How This Works")
    st.markdown("This AI system simulates a small **Agent Society** that learns and validates knowledge collaboratively:")
    st.markdown("---")

    st.subheader("👨‍🎓 Student Agent")
    st.markdown("""
    - Asks questions based on the topic.
    - Always seeks knowledge from the teaching Agent.
    """)

    st.subheader("👨‍🏫 Teacher Agent")
    st.markdown("""
    - Provides explanations based on trusted sources like **Khan Academy** and **YouTube**.
    - Always replies to the Student Agent's questions.
    """)

    st.subheader("🧪 Validator Agent")
    st.markdown("""
    - Evaluates the **Teacher's explanation**.
    - Checks for **accuracy**, clarity, and missing points.
    - Ensures the Student learns correct info.
    """)

    st.markdown("---")
    st.markdown("Together, these agents form a **closed loop** where knowledge is requested, taught, and tested just like in real educational settings.")

