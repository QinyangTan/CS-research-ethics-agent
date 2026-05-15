.PHONY: test benchmark benchmark-score check-no-llm

test:
	pytest

benchmark:
	python3 benchmarks/scripts/generate_fixtures.py
	python3 benchmarks/scripts/run_repo_ethics_benchmark.py

benchmark-score:
	python3 benchmarks/scripts/score_reports.py
	python3 benchmarks/scripts/summarize_results.py
	python3 benchmarks/scripts/write_direct_comparison_report.py

check-no-llm:
	python3 scripts/check_no_hosted_llm_calls.py
