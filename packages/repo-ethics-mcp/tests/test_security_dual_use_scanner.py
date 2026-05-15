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

