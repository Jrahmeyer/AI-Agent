# AI-Agent
# Agentic Debugging Tool (Python)

An LLM-powered code agent that reads, edits, and runs code to propose fixes, refactors, and small features via safe tool-calling.

## Features
- Plan → Execute → Verify loop for iterative debugging
- File I/O, test runner, formatter/linter tools
- Sandboxed command execution and scoped filesystem access
- Git integration: branch, commit, and PR-ready changes
- Structured logging for traceability

# Quick Start
1. Clone the repo
```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

3. Create and activate a virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

4. Install dependencies
pip install -r requirements.txt

5. Set environment variables
export OPENAI_API_KEY=...     # or GEMINI_API_KEY=...
optional
export AGENT_MODEL=gpt-4o-mini

6. Run the agent
python -m agent.run --repo ./target_repo --task "Fix failing tests"

# Usage
* Target a directory:
python -m agent.run --repo ./my_project --task "Refactor function X for readability"

* Dry run (no file writes):
python -m agent.run --repo ./my_project --task "Suggest fixes" --dry-run

* Limit tools (safer):
python -m agent.run --repo ./my_project --task "Run tests" --tools file,tests

See python -m agent.run --help for all flags.

## Safety
No network/file deletions without explicit confirmation
Command sandboxing (blocked: rm -rf, curl | sh, etc.)
Scoped access to --repo path only
Use at your own risk; review diffs before committing.

# Git Workflow
git checkout -b agent/<short-task>
python -m agent.run --repo ./target_repo --task "..."
git add -A
git commit -m "agent: <summary>"
git push -u origin agent/<short-task>

# Configuration
config.yaml: model, max tokens, tool allowlist, timeouts
.agentignore: paths the agent must not touch
prompts/: system and tool-specific prompts
# Extending
Add a tool:
Create tools/<name>.py with run(input) -> output
Register in tools/__init__.py
Allow via --tools <name> or config.yaml

# Logs
logs/session-*.jsonl with step-by-step traces
reports/ for summaries and diffs

# Examples
Fix tests
python -m agent.run --repo ./examples/flaky --task "Diagnose failing tests"

Refactor module
python -m agent.run --repo ./examples/pkg --task "Extract function and add docstrings" --dry-run

# Requirements
Python 3.10+
API key for your chosen LLM provider

# Disclaimer
This is a research/toy tool. Review changes; do not run on sensitive codebases.
