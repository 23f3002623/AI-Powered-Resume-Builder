"""Defines the shared Gemini LLM and the three specialised agents."""
import os

from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

# One LLM object shared by every agent so behaviour stays consistent.
# Everything is configured from the .env file:
#   - Gemini (default):  GEMINI_API_KEY (+ optional GEMINI_MODEL)
#   - Groq / any OpenAI-compatible provider: LLM_API_KEY, LLM_BASE_URL, GEMINI_MODEL
gemini_llm = LLM(
    model="openai/openai/gpt-oss-120b",
    api_key=os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL") or None,
    temperature=0.3,
)

def audit_specialist() -> Agent:
    """Agent 1: compares the profile with the job description."""
    return Agent(
        role="ATS Intelligence Analyst",
        goal="Evaluate candidate vs JD",
        backstory=(
            "You are an expert in Applicant Tracking Systems. You know how "
            "keyword matching works and you can spot missing skills, tools "
            "and phrases in a profile compared with a job posting."
        ),
        llm=gemini_llm,
        memory=True,
        verbose=True,
    )


def resume_architect() -> Agent:
    """Agent 2: rewrites the resume for the job."""
    return Agent(
        role="Executive Resume Architect",
        goal="Rewrite achievements into a tailored, ATS-friendly resume",
        backstory=(
            "You are a professional resume writer who turns plain project "
            "descriptions into short, impact-focused bullet points that use "
            "the keywords of the job description. You never invent skills "
            "or experience that the candidate does not have."
        ),
        llm=gemini_llm,
        memory=True,
        verbose=True,
    )


def career_mentor() -> Agent:
    """Agent 3: plans how to improve the profile further."""
    return Agent(
        role="Technical Career Mentor",
        goal="Plan skills, projects and quick fixes to improve the profile",
        backstory=(
            "You are a senior engineer who mentors students. You give "
            "practical, step-by-step advice: what to learn, what to build "
            "and what small resume fixes to make right now."
        ),
        llm=gemini_llm,
        memory=True,
        verbose=True,
    )
