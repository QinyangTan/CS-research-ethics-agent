.PHONY: test benchmark benchmark-score

test:
	pytest

benchmark:
	python3 benchmarks/scripts/generate_fixtures.py
	python3 benchmarks/scripts/run_repo_ethics_benchmark.py

benchmark-score:
	python3 benchmarks/scripts/score_reports.py
