.PHONY: test benchmark benchmark-score benchmark-analyze check-no-llm sanitize-benchmark-outputs

test:
	pytest

benchmark:
	python3 benchmarks/scripts/generate_fixtures.py
	python3 benchmarks/scripts/run_repo_ethics_benchmark.py

benchmark-score:
	python3 benchmarks/scripts/score_reports.py
	python3 benchmarks/scripts/summarize_results.py
	python3 benchmarks/scripts/write_direct_comparison_report.py

benchmark-analyze:
	python3 benchmarks/scripts/analyze_underperformance.py

sanitize-benchmark-outputs:
	python3 benchmarks/scripts/sanitize_benchmark_outputs.py
	python3 benchmarks/scripts/sanitize_benchmark_outputs.py --check

check-no-llm:
	python3 scripts/check_no_hosted_llm_calls.py
