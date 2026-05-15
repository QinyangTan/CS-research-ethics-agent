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
BASELINES = {
    "strong": {
        "prompt_path": REPO_ROOT / "benchmarks" / "prompts" / "direct_codex_prompt.md",
        "output_dir": REPO_ROOT / "benchmarks" / "outputs" / "direct_codex",
    },
    "naive": {
        "prompt_path": REPO_ROOT / "benchmarks" / "prompts" / "direct_codex_naive_prompt.md",
        "output_dir": REPO_ROOT / "benchmarks" / "outputs" / "direct_codex_naive",
    },
}


def load_cases(cases_path: Path) -> list[dict]:
    return [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare or optionally run direct Codex baseline collection.")
    parser.add_argument("--cases", type=Path, default=REPO_ROOT / "benchmarks" / "cases" / "cs_ethics_cases.jsonl")
    parser.add_argument("--baseline", choices=sorted(BASELINES), default="strong")
    parser.add_argument("--prompt-path", type=Path, default=None, help="Override the prompt path for this collection run.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Override the output directory for this collection run.")
    parser.add_argument(
        "--direct-codex-command",
        default=None,
        help=(
            "Opt-in local command template using {fixture_path}, {prompt_path}, {output_path}. "
            "This is executed on your machine; review it carefully."
        ),
    )
    args = parser.parse_args()
    baseline_defaults = BASELINES[args.baseline]
    prompt_path = args.prompt_path or baseline_defaults["prompt_path"]
    output_dir = args.output_dir or baseline_defaults["output_dir"]

    cases = [case for case in load_cases(args.cases) if case.get("review_status") == "reviewed"]
    output_dir.mkdir(parents=True, exist_ok=True)
    if not args.direct_codex_command:
        print("No direct Codex command was run.")
        print(f"Baseline: {args.baseline}")
        print(f"For each fixture, run your local Codex setup with {prompt_path}.")
        print(f"Save Markdown outputs as {output_dir}/<case_id>.md.")
        print("This workflow is intentionally opt-in because Codex CLI syntax varies by local setup.")
        print("If you pass --direct-codex-command, that local command is executed by this script; review it carefully first.")
        print(f"Reviewed cases ready for collection: {len(cases)}")
        return

    for case in cases:
        fixture_path = REPO_ROOT / case["fixture_path"]
        output_path = output_dir / f"{case['case_id']}.md"
        command = args.direct_codex_command.format(
            fixture_path=shlex.quote(str(fixture_path)),
            prompt_path=shlex.quote(str(prompt_path)),
            output_path=shlex.quote(str(output_path)),
        )
        subprocess.run(command, shell=True, check=True)
    print(f"Collected {len(cases)} {args.baseline} direct Codex outputs in {output_dir}")


if __name__ == "__main__":
    main()
