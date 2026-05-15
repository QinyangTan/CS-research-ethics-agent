from repo_ethics.scanners.file_classifier import classify_file


def test_file_classifier_common_paths() -> None:
    assert classify_file("README.md") == "project_description"
    assert classify_file("src/app.py") == "source_code"
    assert classify_file("data/schema.json") == "data_schema"
    assert classify_file("LICENSE") == "license"
    assert classify_file("docs/usage.md") == "documentation"
    assert classify_file("SECURITY.md") == "security_policy"
    assert classify_file("pyproject.toml") == "dependency_manifest"

