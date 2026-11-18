# AI-Powered Resume Builder & Optimization

A command-line tool that uses three CrewAI agents (Gemini 2.0 Flash) to compare a
student profile with a job description and then produce:

| Agent | Output |
|---|---|
| ATS Intelligence Analyst | `output/ats_report.md` |
| Executive Resume Architect | `output/resume.md` |
| Technical Career Mentor | `output/improvement_plan.md` |

## Setup (one time)

Requires Python 3.10 – 3.13 (3.12 recommended) and a free Gemini API key
from https://aistudio.google.com/apikey

### Windows (PowerShell / CMD)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Linux / macOS
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Get a free key at https://console.groq.com/keys, open `.env` and replace `your_groq_key_here` with it (no spaces, no quotes).

## Run

```
python -m ai_resume_builder.main
```

Run it from the project root (the folder that contains `input/` and `output/`).

## Screenshots for the report
Take them in this order and save in `screenshots/` (see `screenshots/README.txt`):
1. `input/` files open in an editor
2. Terminal while the command runs
3. `output/ats_report.md`, `output/resume.md`, `output/improvement_plan.md`

## Use your own data
Edit `input/job_description.txt` and `input/student_profile.txt`, then run again.

## Troubleshooting
- **GEMINI_API_KEY is missing** – create `.env` from `.env.example` and add the key.
- **Model not found / 404** – Google may have retired the model. Set
  `GEMINI_MODEL=gemini/gemini-2.5-flash` in `.env`.
- **429 / quota error** – wait a minute and run again (free-tier limits).
