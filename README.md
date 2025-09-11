# CareerGuide AI Career Advisor

A fully local, privacy-friendly career advisor bot. 
**Stack:** Python · Streamlit · llama.cpp (via `llama-cpp-python`) · SQLite · Git

## Snap 

<img width="1584" height="693" alt="Screenshot from 2025-09-11 19-44-42" src="https://github.com/user-attachments/assets/d85c5679-d8d8-4001-a44c-ce75df30186f" />


## How to run 

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How it work 
When you pose a question, the app directs it to a basic intent detector (e.g., skills, learning path, resume). A short preamble is created from that intent, and along with your last few chat turns, it constitutes the final prompt.  A small, chat-tuned GGUF model is loaded locally using llama-cpp-python to produce the answer—no data exits your machine.  The response is displayed in chat bubbles by Streamlit, which also shows a “thinking locally” status while the model is running.  All exchanges along with any thumbs-up/down feedback are recorded in a local SQLite database, ensuring that session history and basic analytics remain entirely on the device.
