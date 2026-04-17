"""Optional OpenAI-powered enhancement layer for ResearchToolAgent."""

from __future__ import annotations

import importlib
import json
import os

from core.schemas import PlanSection, ResearchSpec


def _resolve_provider(provider: str) -> str:
    normalized = provider.lower().strip()
    if normalized == "自动":
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        if os.getenv("QWEN_API_KEY"):
            return "qwen"
        return "openai"
    return normalized


def _provider_config(provider: str) -> tuple[str, str | None, str]:
    normalized = _resolve_provider(provider)
    if normalized == "qwen":
        return (
            os.getenv("QWEN_API_KEY", ""),
            os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            os.getenv("QWEN_MODEL", "qwen-plus"),
        )
    return (
        os.getenv("OPENAI_API_KEY", ""),
        os.getenv("OPENAI_BASE_URL"),
        os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    )


def is_ai_ready(provider: str) -> tuple[bool, str, str]:
    """Check whether selected provider, SDK and API key are available."""
    chosen_provider = _resolve_provider(provider)
    api_key, _, _ = _provider_config(chosen_provider)
    has_key = bool(api_key)
    if not has_key:
        if chosen_provider == "qwen":
            return False, "未检测到 QWEN_API_KEY（请先配置后再生成）。", chosen_provider
        return False, "未检测到 OPENAI_API_KEY（请先配置后再生成）。", chosen_provider

    try:
        importlib.import_module("openai")
    except ModuleNotFoundError:
        return False, "未安装 openai SDK，请先安装 requirements.txt 依赖。", chosen_provider

    return True, f"已启用大模型增强输出（{chosen_provider.upper()}）。", chosen_provider


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


def enhance_plan_with_ai(spec: ResearchSpec, sections: list[PlanSection], provider: str) -> dict | None:
    """Return AI-enhanced plan payload, or None when API output is invalid."""
    ready, _, chosen_provider = is_ai_ready(provider)
    if not ready:
        return None

    api_key, base_url, model = _provider_config(chosen_provider)
    openai_module = importlib.import_module("openai")
    client = openai_module.OpenAI(api_key=api_key, base_url=base_url)

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
