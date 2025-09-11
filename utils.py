
import uuid
import streamlit as st

def get_session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def badge(text: str):
    return f'<span class="badge">{text}</span>'

def inject_css():
    st.markdown(
        """
        <style>
           
            .main .block-container { max-width: 900px; }
            .stApp { background: radial-gradient(1200px 600px at 10% 10%, #0b1220 0, #070b14 40%, #05070d 100%); color: #e6ecff; }
            h1, h2, h3 { letter-spacing: 0.2px; }
            .title {
                display:flex; align-items:center; gap:0.8rem; margin-bottom:0.4rem;
            }
            .title .dot {
                width: 12px; height: 12px; border-radius: 50%;
                background: linear-gradient(135deg,#6ee7ff,#a78bfa);
                box-shadow: 0 0 18px #6ee7ff55;
            }
            .subtitle { opacity: 0.8; margin-bottom: 1rem; }
            .glass {
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px; padding: 16px 18px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            }
            .badge {
                display:inline-block; padding:4px 10px; border-radius:999px;
                background: rgba(167,139,250,0.14);
                border: 1px solid rgba(167,139,250,0.35);
                color: #c7b9ff; font-size: 12px; margin-right: 6px;
            }
            .chip{
                display:inline-block; padding:8px 12px; border-radius:999px;
                border: 1px dashed rgba(255,255,255,0.25);
                margin: 4px 6px; font-size: 13px; opacity: 0.9;
            }
            .assistant-bubble {
                background: rgba(110, 231, 255, 0.06);
                border: 1px solid rgba(110, 231, 255, 0.28);
                border-radius: 16px; padding: 14px 16px; margin: 8px 0;
            }
            .user-bubble {
                background: rgba(167, 139, 250, 0.08);
                border: 1px solid rgba(167, 139, 250, 0.28);
                border-radius: 16px; padding: 14px 16px; margin: 8px 0;
            }
            .small { font-size: 12px; opacity: 0.7; }
        </style>
        """,
        unsafe_allow_html=True,
    )
