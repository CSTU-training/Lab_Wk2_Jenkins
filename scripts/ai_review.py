#!/usr/bin/env python3
"""
AI code review step for the CSE636 Week 2 lab.

The script reads Python files changed in the most recent commit and asks
Claude to review them for correctness, style issues, and potential bugs.
"""

import os
import subprocess
from pathlib import Path

import anthropic


def get_changed_files() -> list[str]:
    """Return Python files changed in the most recent Git commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        # A repository with only one commit does not have HEAD~1.
        # In that case, review every tracked Python file.
        fallback = subprocess.run(
            ["git", "ls-files", "*.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        output = fallback.stdout
    else:
        output = result.stdout

    return [
        filename
        for filename in output.strip().splitlines()
        if filename.endswith(".py")
    ]


def read_file(path: str) -> str | None:
    """Read a UTF-8 source file, returning None if it no longer exists."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def review_code(
    client: anthropic.Anthropic,
    filename: str,
    content: str,
) -> str:
    """Ask Claude to review one Python source file."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Please review the following Python file for correctness, "
                    "style issues, security concerns, missing edge-case handling, "
                    "and potential bugs. Be concise and specific.\n\n"
                    f"Filename: {filename}\n\n"
                    f"```python\n{content}\n```"
                ),
            }
        ],
    )

    return message.content[0].text


def main() -> None:
    """Generate ai_review_report.txt for changed Python files."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is missing.")

    client = anthropic.Anthropic(api_key=api_key)
    changed_files = get_changed_files()

    if not changed_files:
        print("No Python files changed. Skipping AI review.")
        Path("ai_review_report.txt").write_text(
            "No Python files changed in this commit.\n",
            encoding="utf-8",
        )
        return

    report_lines = ["# AI Code Review Report\n"]

    for filepath in changed_files:
        content = read_file(filepath)
        if content is None:
            continue

        print(f"Reviewing {filepath}...")
        review = review_code(client, filepath, content)
        report_lines.append(f"\n## {filepath}\n\n{review}\n")
        print(f"Review for {filepath}:\n{review}\n")

    Path("ai_review_report.txt").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )
    print("AI review complete. Report saved to ai_review_report.txt")


if __name__ == "__main__":
    main()
