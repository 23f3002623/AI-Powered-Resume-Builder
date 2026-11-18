"""Joins the agents and tasks into one sequential crew."""
from crewai import Crew, Process

from .agents import audit_specialist, career_mentor, resume_architect
from .tasks import audit_task, resume_task, roadmap_task


class ResumeOptimizationCrew:
    def __init__(self, job_desc: str, profile: str):
        self.job_desc = job_desc
        self.profile = profile

    def build(self) -> Crew:
        auditor = audit_specialist()
        architect = resume_architect()
        mentor = career_mentor()

        task_audit = audit_task(auditor, self.job_desc, self.profile)
        task_resume = resume_task(
            architect, self.job_desc, self.profile, context=[task_audit]
        )
        task_roadmap = roadmap_task(mentor, context=[task_audit, task_resume])

        return Crew(
            agents=[auditor, architect, mentor],
            tasks=[task_audit, task_resume, task_roadmap],
            process=Process.sequential,
            verbose=True,
        )

    def run(self):
        return self.build().kickoff()
