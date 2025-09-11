# model.py
from __future__ import annotations
from typing import List, Dict, Optional
from pathlib import Path
import re
from llama_cpp import Llama

# Default model path (update if you use another model)
DEFAULT_MODEL_PATH = "./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

_llm: Optional[Llama] = None

FORBIDDEN_HEADINGS = [
    "purpose", "style", "guardrails", "do not", "output format", "quality hints",
    "context", "output requirements"
]

def _resolve_model_path() -> str:
    p = Path(DEFAULT_MODEL_PATH)
    if p.exists():
        return str(p)
    models_dir = Path(__file__).resolve().parent / "models"
    ggufs = sorted(models_dir.glob("*.gguf"))
    if not ggufs:
        raise ValueError(f"No .gguf model found in {models_dir}")
    return str(ggufs[0])

def load_llm(model_path: str = DEFAULT_MODEL_PATH, n_ctx: int = 2048, n_gpu_layers: int = 0) -> Llama:
    """
    Use a chat_format that tiny chat models obey. TinyLlama usually works with 'chatml'.
    If it still echoes, try chat_format='tinyllama' or 'llama-2'.
    """
    global _llm
    if _llm is None:
        resolved_path = _resolve_model_path()
        _llm = Llama(
            model_path=resolved_path,
            n_ctx=n_ctx,
            n_threads=None,        # auto
            n_gpu_layers=n_gpu_layers,  # 0 = CPU-only
            use_mmap=True,
            use_mlock=False,
            verbose=False,
            chat_format="chatml",  # TRY this first; alternatives: "tinyllama", "llama-2"
            repeat_penalty=1.08,
            penalize_nl=True,
        )
    return _llm

def _looks_like_echo(text: str) -> bool:
    head = text.strip()[:600].lower()
    return any(h in head for h in FORBIDDEN_HEADINGS) or "i am careerguide" in head

def chat(
    system_prompt: str,
    user_prompt: str,
    history: List[Dict[str, str]],
    temperature: float = 0.3,
    top_p: float = 0.9,
    max_tokens: int = 512,
) -> str:
    """
    Run a chat completion with local llama.cpp model.
    history: list of {role: 'user'|'assistant', content: str}
    """
    llm = load_llm()

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_prompt})

    out = llm.create_chat_completion(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    answer = out["choices"][0]["message"]["content"].strip()

    # Fallback: if the model echoed instructions, re-ask crisply without the big system block
    if _looks_like_echo(answer):
        fallback_messages = [
            {
                "role": "system",
                "content": (
                    "You are a concise career advisor. Answer the user directly in bullets. "
                    "Do not repeat or reference any meta-instructions or headings."
                ),
            },
            {"role": "user", "content": user_prompt},
        ]
        out2 = llm.create_chat_completion(
            messages=fallback_messages,
            temperature=0.2,
            top_p=0.9,
            max_tokens=max_tokens,
        )
        answer = out2["choices"][0]["message"]["content"].strip()

    return answer
