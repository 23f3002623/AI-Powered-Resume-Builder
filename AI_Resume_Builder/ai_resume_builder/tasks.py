"""Defines the three tasks and the output file of each one."""
from pathlib import Path

from crewai import Agent, Task

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def audit_task(agent: Agent, job_desc: str, profile: str) -> Task:
    return Task(
        description=(
            "Gap analysis.\n"
            "Compare the student profile with the job description.\n"
            "1. Give an ATS compatibility score out of 100%.\n"
            "2. List the matched skills.\n"
            "3. List the missing keywords, skills and tools.\n"
            "4. Add a short summary.\n\n"
            f"JOB: {job_desc}\n\n"
            f"PROFILE: {profile}"
        ),
        expected_output="ATS report (markdown)",
        agent=agent,
        output_file=str(OUTPUT_DIR / "ats_report.md"),
    )


def resume_task(agent: Agent, job_desc: str, profile: str, context: list) -> Task:
    return Task(
        description=(
            "Using the ATS report from the previous task, write a tailored, "
            "ATS-friendly resume in Markdown for this job. Use these sections: "
            "Name and contact, Summary, Technical Skills, Projects, Education. "
            "Rewrite achievements with strong action verbs and the keywords "
            "of the job description. Only use facts present in the profile; "
            "do not invent skills, projects or numbers.\n\n"
            f"JOB: {job_desc}\n\n"
            f"PROFILE: {profile}"
        ),
        expected_output="Tailored resume (markdown)",
        agent=agent,
        context=context,
        output_file=str(OUTPUT_DIR / "resume.md"),
    )


def roadmap_task(agent: Agent, context: list) -> Task:
    return Task(
        description=(
            "Using the ATS report and the tailored resume, prepare an "
            "improvement roadmap in Markdown with three parts: "
            "(1) skills to learn, (2) projects to build that cover the "
            "missing keywords, (3) quick fixes for the resume. "
            "Keep the plan practical and in a sensible order."
        ),
        expected_output="Improvement roadmap (markdown)",
        agent=agent,
        context=context,
        output_file=str(OUTPUT_DIR / "improvement_plan.md"),
    )
