"""Pydantic schemas for ResearchToolAgent."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ResearchSpec(BaseModel):
    """Structured requirement inferred from user prompt and form inputs."""

    project_name: str = Field(default="UntitledResearchTool")
    problem_statement: str
    task_type: str
    input_format: str
    output_format: str
    needs_training: bool = False
    deployment_form: str
    github_sync: bool = False
    deliverables: List[str]


class PlanSection(BaseModel):
    """A section in the generated design plan."""

    title: str
    items: List[str]


class ScaffoldEntry(BaseModel):
    """Path and purpose for project scaffold explanation."""

    path: str
    purpose: str


class ScaffoldSuggestion(BaseModel):
    """Text tree and details for recommended project structure."""

    tree: str
    descriptions: List[ScaffoldEntry]
