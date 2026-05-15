from pathlib import Path

from repo_ethics.scanners.security_dual_use_scanner import scan


def test_security_scanner_detects_cve_exploit_and_socket_scanning(tmp_path: Path) -> None:
    code = tmp_path / "scanner.py"
    code.write_text(
        "import socket\n# exploit check for CVE-2025-0001\nsock = socket.socket(); sock.connect_ex(('host', 80))\n",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    reasons = " ".join(item.reason for item in evidence)
    assert "exploit" in reasons
    assert "CVEs" in reasons
    assert "socket scanning" in reasons


def test_security_scanner_ignores_negated_vulnerability_scanner(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("This is not a vulnerability scanner.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.category == "security_dual_use"]


def test_security_scanner_detects_contrastive_vulnerability_scanner(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("This is not a toy and it is a vulnerability scanner.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(item.category == "security_dual_use" for item in evidence)


def test_security_scanner_ignores_not_used_for_port_scanning(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("This tool is not used for port scanning.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.category == "security_dual_use"]


def test_security_scanner_detects_contrastive_port_scanning(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("This tool is not used for demos, but it performs port scanning.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(item.category == "security_dual_use" for item in evidence)


def test_security_scanner_ignores_tests_and_docs_tutorial_terms(tmp_path: Path) -> None:
    tests = tmp_path / "tests"
    docs = tmp_path / "docs"
    tests.mkdir()
    docs.mkdir()
    (tests / "test_security.py").write_text("# exploit regression word only\n", encoding="utf-8")
    (docs / "security_tutorial.md").write_text(
        "This tutorial mentions vulnerability scanner examples.",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.category == "security_dual_use"]
