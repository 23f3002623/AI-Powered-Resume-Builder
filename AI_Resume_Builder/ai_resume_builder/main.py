"""Entry point: reads the two input files and starts the pipeline.

Run from the project root with:
    python -m ai_resume_builder.main
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class PipelineInput(BaseModel):
    """Validates that both inputs contain text before any agent starts."""

    job_description: str
    student_profile: str

    @field_validator("job_description", "student_profile")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("input file is empty")
        return value


def fetch_document_content(path: Path) -> str:
    """Read a plain-text input file."""
    if not path.exists():
        sys.exit(f"[ERROR] Input file not found: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    api_key = (os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key or api_key.startswith("your_"):
        sys.exit(
            "[ERROR] API key is missing.\n"
            "Copy .env.example to .env and paste your key after LLM_API_KEY= "
            "(free key: https://console.groq.com/keys)"
        )

    input_dir = BASE_DIR / "input"
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    job_spec = fetch_document_content(input_dir / "job_description.txt")
    profile = fetch_document_content(input_dir / "student_profile.txt")
    data = PipelineInput(job_description=job_spec, student_profile=profile)

    # Imported here so a missing key is reported before CrewAI starts.
    from .crew import ResumeOptimizationCrew

    pipeline = ResumeOptimizationCrew(data.job_description, data.student_profile)
    result = pipeline.run()

    print("\n" + "=" * 60)
    print("DONE. Files saved in the output/ folder:")
    for name in ("ats_report.md", "resume.md", "improvement_plan.md"):
        print("  -", output_dir / name)
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
