
import os
import base64
import streamlit as st
from utils import badge

def _robot_data_uri(path: str = "assets/robot.png") -> str | None:
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    return None

def load_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp { background: #fafafa    ; color: #0f172a; }
            .main .block-container { max-width: 900px; position: relative; z-index: 2; }

            .title { display:flex; align-items:center; gap:0.75rem; margin-bottom:0.25rem; }
            .title .dot { width:12px; height:12px; border-radius:50%; background:#5b21b6; box-shadow:0 0 14px #5b21b677; }
            .subtitle { color:#475569; margin-bottom:0.75rem; }

            .bg-art { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
            .bg-art::before,
            .bg-art::after{ content:""; position: absolute; width: 56vmax; height: 56vmax; border-radius: 50%; background: #5b21b6; }
            .bg-art::before{ top: -38vmax; left: -38vmax; box-shadow: 0 20px 60px rgba(91,33,182,0.25); }
            .bg-art::after{ right: -42vmax; bottom: -42vmax; box-shadow: 0 -20px 60px rgba(91,33,182,0.25); }


            .bg-art img.bot{
                position: fixed;
                right: clamp(12px, 3vw, 40px);
                bottom: clamp(12px, 6vh, 64px);
                width: min(320px, 28vw);
                height: auto;
                filter: drop-shadow(0 18px 32px rgba(2,6,23,0.25));
                user-select: none;
            }

            .card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 16px; padding: 8px 10px; box-shadow: 0 4px 14px rgba(2,6,23,0.06); }
            .card h4 { margin: 0 0 8px 0; font-size: 1rem; color:#111827; }
            .muted { color:#64748b; font-size: 0.9rem; }

            .stButton > button { background: #5b21b6    ; color: #ffffff    ; border: 1px solid #4c1d95    ; border-radius: 12px    ; padding: 0.55rem 0.9rem    ; box-shadow: 0 6px 18px rgba(91,33,182,0.18)    ; }
            .stButton > button:hover { filter: brightness(1.05); }

            div[data-baseweb="slider"] > div { color: #5b21b6    ; }
            div[data-baseweb="slider"] div[role="slider"] { background: #5b21b6    ; border: 2px solid #5b21b6    ; box-shadow: 0 0 0 4px rgba(91,33,182,0.18)    ; }
            div[data-baseweb="slider"] > div > div { background: linear-gradient(90deg, #5b21b6 0%, #7c3aed 100%)    ; }

            div[role="radiogroup"] > div[aria-label="radio-group"] { gap: 8px; }
            div[role="radiogroup"] label { border-radius: 999px    ; border: 1px solid #e5e7eb    ; background: #fff    ; padding: 6px 12px    ; box-shadow: 0 2px 8px rgba(2,6,23,0.04)    ; }
            div[role="radiogroup"] input:checked + div { color:#5b21b6     ; border-color:#4c1d95    ; }

            .bubble { border-radius: 14px; padding: 12px 14px; margin: 10px 0; border:1px solid #edeef2; }
            .user-bubble { background:#f5f3ff; border-color:#e9d5ff; }
            .assistant-bubble { background:#eef2ff; border-color:#c7d2fe; }
            .bubble-meta { font-size:12px; color:#6b7280; margin-bottom:6px; }

            .feedback-row .stButton > button { padding: 0.4rem 0.6rem    ; border-radius:10px    ; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def show_bg() -> None:
    uri = _robot_data_uri("assets/robot.png")
    if uri:
        st.markdown(
            f"""
            <div class="bg-art">
                <div class="white-canvas"></div>
                <img class="bot" src="{uri}" alt="bot"/>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="bg-art">
                <div class="white-canvas"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def page_header() -> None:
    st.markdown(
        """
        <div class="title">
            <div class="dot"></div>
            <h1 style="margin:0">CareerGuide</h1>
        </div>
        <div class="subtitle"> llama.cpp-powered career advisor.</div>
        """,
        unsafe_allow_html=True,
    )

def chat_bubble(message_id, role, intent_name, text, timestamp) -> None:
    bubble_class = "assistant-bubble" if role == "assistant" else "user-bubble"
    st.markdown(
        f'<div class="bubble {bubble_class}">'
        f'<div class="bubble-meta">{badge(intent_name)} {timestamp}</div>'
        f'<div>{text}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
