"""Optional direct-Codex baseline workflow.

By default this script only prints instructions. It runs a command only when
the evaluator explicitly provides --direct-codex-command.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_cases(cases_path: Path) -> list[dict]:
    return [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or optionally run direct Codex baseline collection.")
    parser.add_argument("--cases", type=Path, default=REPO_ROOT / "benchmarks" / "cases" / "cs_ethics_cases.jsonl")
    parser.add_argument("--prompt-path", type=Path, default=REPO_ROOT / "benchmarks" / "prompts" / "direct_codex_prompt.md")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "benchmarks" / "outputs" / "direct_codex")
    parser.add_argument("--direct-codex-command", default=None, help="Opt-in command template using {fixture_path}, {prompt_path}, {output_path}.")
    args = parser.parse_args()

    cases = [case for case in load_cases(args.cases) if case.get("review_status") == "reviewed"]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if not args.direct_codex_command:
        print("No direct Codex command was run.")
        print("For each fixture, run your local Codex setup with benchmarks/prompts/direct_codex_prompt.md.")
        print("Save Markdown outputs as benchmarks/outputs/direct_codex/<case_id>.md.")
        print("This workflow is intentionally opt-in because Codex CLI syntax varies by local setup.")
        print(f"Reviewed cases ready for collection: {len(cases)}")
        return

    for case in cases:
        fixture_path = REPO_ROOT / case["fixture_path"]
        output_path = args.output_dir / f"{case['case_id']}.md"
        command = args.direct_codex_command.format(
            fixture_path=shlex.quote(str(fixture_path)),
            prompt_path=shlex.quote(str(args.prompt_path)),
            output_path=shlex.quote(str(output_path)),
        )
        subprocess.run(command, shell=True, check=True)
    print(f"Collected {len(cases)} direct Codex outputs in {args.output_dir}")


if __name__ == "__main__":
    main()
