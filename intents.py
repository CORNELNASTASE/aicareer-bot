
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
import re

@dataclass
class Intent:
    name: str
    description: str

INTENT_DEFS: List[Intent] = [
    Intent("skills_for_role", "What skills are required for a specific job title."),
    Intent("popular_roles",  "What roles are popular in a given field."),
    Intent("resume_help",    "How to improve a resume or CV."),
    Intent("learning_path",  "How to learn or transition into a role."),
    Intent("interview_prep", "How to prepare for interviews in a domain."),
    Intent("career_switch",  "How to switch careers or industries."),
    Intent("general_guidance","General career questions."),
]

# --- Keyword routing  ---


RULES = [
    ("skills_for_role", [
        "skills for", "required skills", "what skills", "skillset",
        "competencies", "tools needed", "tech stack for",
    ]),
    ("popular_roles", [
        "popular roles", "in-demand", "trending roles", "hot roles",
        "market demand", "growth roles",
    ]),
    ("resume_help", [
        "resume", "cv", "cover letter", "ats", "bullet points", "portfolio tips",
    ]),
    ("learning_path", [
        "learn", "roadmap", "road map", "read map", "how to become",
        "path", "syllabus", "curriculum", "step by step",
    ]),
    ("interview_prep", [
        "interview", "questions", "behavioral", "system design",
        "coding round", "mock interview", "hire manager", "hr round",
    ]),
    ("career_switch", [
        "switch career", "career change", "transition", "cross-skill",
        "move into", "break into",
    ]),
]

# --- Intent templates   ---

INTENT_TEMPLATES = {
    "skills_for_role":  "Focus on core skills, tools, and typical experience for the role: {query}. Provide concrete, actionable next steps.",
    "popular_roles":    "Focus on in-demand and growing roles in the field: {query}. Offer brief role snapshots and suggested first steps.",
    "resume_help":      "Provide resume/CV guidance tailored to: {query}. Include bullet examples and quick ATS-friendly tips.",
    "learning_path":    "Provide a concise learning roadmap for: {query}. Include skills, tools, projects, and practice ideas.",
    "interview_prep":   "Offer interview preparation guidance for: {query}. Include common topics, practice prompts, and tips.",
    "career_switch":    "Give a transition plan to move into: {query}. Include skill gaps, bridging projects, and first steps.",
    "general_guidance": "Offer practical career guidance about: {query}. Provide next steps and focused practice ideas.",
}

# --- Helpers ----

PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)

def _normalize(text: str) -> str:
    """Lowercase, fix common typos, strip punctuation/extra spaces."""
    t = (text or "").lower()
    t = t.replace("read map", "roadmap").replace("road map", "roadmap")
    t = PUNCT_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def _contains_any(haystack: str, needles: list[str]) -> bool:
    return any(n in haystack for n in needles)

# --- Public API -----

def find_intent(text: str) -> str:
    """
    Deterministic keyword router with light normalization.
    Falls back to 'general_guidance' if nothing matches.
    """
    t = _normalize(text)
    for name, keys in RULES:
        if _contains_any(t, keys):
            return name
    return "general_guidance"

def make_system_preamble(intent: str, user_query: str) -> str:
    """
    Returns a compact, instruction-style preamble with NO headings like
    'Context:' or 'Output requirements:' to reduce instruction echoing.
    This string is meant to be appended to your base system prompt.
    """
    base = INTENT_TEMPLATES.get(intent, INTENT_TEMPLATES["general_guidance"]).format(query=user_query)

    return (
        f"{base}\n\n"
        "Answer directly. Start with a 1–2 line summary, then 4–8 compact bullets. "
        "Include skills/tools, learning steps, practice projects, resume/interview tips, and concrete next steps. "
        "Offer generic resource ideas (no external links). "
        "Ask exactly one short clarifying question at the end only if needed. "
        "Do not repeat or reference any instructions."
    )

INTENT_NAMES_FOR_UI = [i.name.replace("_", " ").title() for i in INTENT_DEFS]
