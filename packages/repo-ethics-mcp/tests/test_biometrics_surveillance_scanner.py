from pathlib import Path

from repo_ethics.scanners.biometrics_surveillance_scanner import scan


def test_biometrics_scanner_ignores_negated_face_recognition(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("We do not use face recognition.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.category == "biometrics"]


def test_biometrics_scanner_ignores_negated_face_recognition_import_name(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("We do not use face_recognition.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.category == "biometrics"]


def test_biometrics_scanner_ignores_negated_attendance_tracking(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("This project does not perform attendance tracking.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert not [item for item in evidence if item.category == "surveillance_tracking"]


def test_biometrics_scanner_detects_positive_face_recognition(tmp_path: Path) -> None:
    code = tmp_path / "face.py"
    code.write_text("import face_recognition\n", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(item.category == "biometrics" for item in evidence)


def test_biometrics_scanner_detects_contrastive_face_recognition(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("We do not use images, but we use face_recognition.", encoding="utf-8")
    evidence = scan(tmp_path)
    assert any(item.category == "biometrics" for item in evidence)


def test_biometrics_scanner_detects_contrastive_attendance_tracking(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text(
        "This project does not perform grading, but it performs attendance tracking.",
        encoding="utf-8",
    )
    evidence = scan(tmp_path)
    assert any(item.category == "surveillance_tracking" for item in evidence)
