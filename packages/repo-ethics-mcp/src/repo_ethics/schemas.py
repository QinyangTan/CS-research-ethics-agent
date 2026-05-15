"""Pydantic schemas used by the scanner, report builder, CLI, and MCP tools."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Confidence = Literal["low", "medium", "high"]
FindingStatus = Literal["confirmed", "potential", "unknown"]
Severity = Literal["low", "medium", "high", "critical"]


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    category: str
    file_path: str
    line_start: int | None = None
    line_end: int | None = None
    snippet: str | None = None
    reason: str
    confidence: Confidence


class ProjectProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    root_path: str
    project_name: str
    languages: list[str] = Field(default_factory=list)
    important_files: list[str] = Field(default_factory=list)
    detected_research_activities: list[str] = Field(default_factory=list)
    detected_data_sources: list[str] = Field(default_factory=list)
    possible_human_data: bool = False
    possible_security_sensitive: bool = False
    possible_dual_use: bool = False
    missing_docs: list[str] = Field(default_factory=list)


class RiskFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_id: str
    title: str
    category: str
    status: FindingStatus
    severity: Severity
    confidence: Confidence
    evidence: list[EvidenceItem] = Field(default_factory=list)
    why_it_matters: str
    missing_context: list[str] = Field(default_factory=list)
    recommended_mitigations: list[str] = Field(default_factory=list)
    advisor_or_irb_questions: list[str] = Field(default_factory=list)


class EthicsReviewReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_profile: ProjectProfile
    findings: list[RiskFinding] = Field(default_factory=list)
    global_missing_context: list[str] = Field(default_factory=list)
    safe_release_checklist: list[str] = Field(default_factory=list)
    disclaimer: str


class ScanResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_profile: ProjectProfile
    evidence: list[EvidenceItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

