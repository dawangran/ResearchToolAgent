"""Optional OpenAI-powered enhancement layer for ResearchToolAgent."""

from __future__ import annotations

import importlib
import json
import os

from core.schemas import PlanSection, ResearchSpec


def is_ai_ready() -> tuple[bool, str]:
    """Check whether OpenAI SDK and API key are available."""
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    if not has_key:
        return False, "未检测到 OPENAI_API_KEY，已回退到本地规则模式。"

    try:
        importlib.import_module("openai")
    except ModuleNotFoundError:
        return False, "未安装 openai SDK，已回退到本地规则模式。"

    return True, "已启用大模型增强输出。"


def _build_prompt(spec: ResearchSpec, sections: list[PlanSection]) -> str:
    section_text = "\n".join(
        [f"- {section.title}: {'；'.join(section.items)}" for section in sections]
    )
    return (
        "你是资深科研产品经理与技术负责人，请基于给定规格输出更人性化、可执行的方案。\n"
        "必须输出 JSON，且仅输出 JSON。字段:\n"
        "{\n"
        '  "overview_md": "string, markdown",\n'
        '  "sections": [{"title":"string","items":["string"]}],\n'
        '  "github_actions": ["string"]\n'
        "}\n\n"
        f"结构化规格:\n{spec.model_dump_json(indent=2, ensure_ascii=False)}\n\n"
        f"当前方案草稿:\n{section_text}\n"
    )


def enhance_plan_with_ai(spec: ResearchSpec, sections: list[PlanSection]) -> dict | None:
    """Return AI-enhanced plan payload, or None when unavailable/invalid."""
    ready, _ = is_ai_ready()
    if not ready:
        return None

    openai_module = importlib.import_module("openai")
    client = openai_module.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "你是严谨且务实的 AI 科研研发顾问。",
            },
            {
                "role": "user",
                "content": _build_prompt(spec, sections),
            },
        ],
    )

    content = response.output_text.strip()
    if not content:
        return None

    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, dict):
        return None
    if "overview_md" not in payload or "sections" not in payload:
        return None
    return payload
