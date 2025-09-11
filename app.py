# app.py
import streamlit as st
import pandas as pd

from utils import get_session_id, inject_css
from intents import find_intent, make_system_preamble, INTENT_DEFS
from db import add_message, get_history, add_feedback
from model import chat
from ui import load_styles, show_bg, page_header, chat_bubble

st.set_page_config(page_title="CareerGuideAI", page_icon="👾", layout="centered")

inject_css()
load_styles()
show_bg()
page_header()

session_id = get_session_id()

intent_examples = {
    "Skills For Role": "What skills are required for a junior data analyst?",
    "Popular Roles": "What are the most in-demand roles in data analytics right now?",
    "Resume Help": "Improve my resume summary for an entry-level data analyst.",
    "Learning Path": "Give me a 12-week roadmap to become a data analyst.",
    "Interview Prep": "What topics should I prepare for a data analyst interview?",
    "Career Switch": "I am a teacher moving into data analysis—what’s my transition plan?",
    "General Guidance": "How do I pick between data analytics, data science, and BI?",
}
intent_labels = [i.name.replace("_", " ").title() for i in INTENT_DEFS]

default_intent = "General Guidance"
if "selected_intent" not in st.session_state:
    st.session_state.selected_intent = default_intent

st.markdown("#### Preferences")
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4>Response Style</h4>", unsafe_allow_html=True)
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.30, 0.05, key="temperature")
    max_tokens = st.slider("Max tokens", 128, 1024, 512, 64, key="max_tokens")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h4>Suggested Intents</h4>", unsafe_allow_html=True)

    current_intent = st.session_state.selected_intent
    chosen_intent = st.radio(
        label="Suggested intents",
        options=intent_labels,
        index=intent_labels.index(current_intent),
        horizontal=True,
        label_visibility="collapsed",
        key="intent_radio",
    )
    if chosen_intent != current_intent:
        st.session_state.selected_intent = chosen_intent
        st.session_state.user_query = intent_examples.get(chosen_intent, "")

    st.markdown('<p class="muted" style="margin-top:6px">Tip: select a pill to prefill the box, then edit your exact question.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
input_col, button_col = st.columns([7, 3])
with input_col:
    st.markdown("<div style='height:45px'></div>", unsafe_allow_html=True)
    user_query = st.text_input(
        "Ask about roles, skills, learning paths, resume, or interviews…",
        key="user_query",
        placeholder="e.g., Data analyst roadmap for beginners",
        label_visibility="collapsed",
    )
with button_col:
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    submit = st.button("Guide", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

status_area = st.empty()
top_answer_container = st.container()

history_rows = get_history(session_id, limit=20)
history_sorted = sorted(history_rows, key=lambda r: r[0], reverse=True)

if submit and user_query.strip():
    intent_name = find_intent(user_query)
    system_preamble = make_system_preamble(intent_name, user_query)
    add_message(session_id, "user", intent_name, user_query)

    compact_history = []
    for _id, role, _intent, content, _ts in sorted(history_rows[-4:], key=lambda r: r[0]):
        compact_history.append({"role": role, "content": content})

    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        base_system = f.read()

    system_prompt = base_system
    composed_user_prompt = (
        f"{system_preamble}\n\n"
        f"User question: {user_query}\n"
        f"Answer directly. Start with a 1–2 line summary, then 4–8 compact bullets, "
        f"and end with one clarifying question only if needed."
    )

    with status_area.status("Thinking locally…", expanded=False) as s:
        answer_text = chat(
            system_prompt=system_prompt,
            user_prompt=composed_user_prompt,
            history=compact_history,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        s.update(label="Done", state="complete", expanded=False)

    assistant_id = add_message(session_id, "assistant", intent_name, answer_text)
    with top_answer_container:
        chat_bubble(assistant_id, "assistant", intent_name, answer_text, "just now")

    st.markdown('<div class="feedback-row">', unsafe_allow_html=True)
    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 6])
    with fb_col1:
        if st.button("Helpful", key=f"up_{assistant_id}"):
            add_feedback(assistant_id, +1, None)
            st.success("Thanks for the feedback!")
    with fb_col2:
        if st.button("Not great", key=f"down_{assistant_id}"):
            add_feedback(assistant_id, -1, None)
            st.info("Feedback noted.")
    with fb_col3:
        feedback_note = st.text_input("Optional comment about this answer", key=f"c_{assistant_id}")
        if st.button("Save comment", key=f"cs_{assistant_id}"):
            add_feedback(assistant_id, 0, feedback_note or "")
            st.success("Comment saved.")
    st.markdown('</div>', unsafe_allow_html=True)

if history_sorted:
    st.markdown("#### Conversation")
    latest_assistant_id = None
    if history_sorted and history_sorted[0][1] == "assistant":
        latest_assistant_id = history_sorted[0][0]
    for msg_id, role, intent_name, text, created_at in history_sorted:
        if latest_assistant_id is not None and msg_id == latest_assistant_id:
            continue
        chat_bubble(msg_id, role, intent_name, text, created_at)
