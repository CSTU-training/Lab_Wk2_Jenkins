# Sample Python App

A minimal Python project for the CSE636 Week 2 Jenkins and AI code review lab.

## Project structure

```text
sample-python-app/
├── app/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   └── test_calculator.py
├── scripts/
│   └── ai_review.py
├── Jenkinsfile
├── requirements-dev.txt
└── README.md
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 -m flake8 app tests scripts --max-line-length=120
python3 -m pytest tests/ -v
```

## Run the AI review locally

Export your Anthropic API key and run:

```bash
export ANTHROPIC_API_KEY="your-key"
python3 scripts/ai_review.py
```

The script creates:

```text
ai_review_report.txt
```

## Jenkins configuration

Before using the Jenkinsfile, replace:

```text
YOUR_GITHUB_USERNAME
```

with your GitHub username.

In Jenkins Credentials, create a Secret text credential with this ID:

```text
ANTHROPIC_API_KEY
```

## Lab observation

The current tests verify normal addition and division. They do not test division
by zero, so the test stage passes while an AI reviewer may identify the missing
edge-case handling. This creates a useful example for the reflection section.
