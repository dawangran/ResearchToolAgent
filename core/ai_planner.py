"""Optional OpenAI-powered enhancement layer for ResearchToolAgent."""

from __future__ import annotations

import importlib
import json
import os
from typing import Any

from core.schemas import PlanSection, ResearchSpec


ProviderOverrides = dict[str, str]


def _resolve_provider(provider: str) -> str:
    normalized = provider.lower().strip()
    if normalized == "自动":
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        if os.getenv("QWEN_API_KEY"):
            return "qwen"
        return "openai"
    return normalized


def _provider_config(provider: str, overrides: ProviderOverrides | None = None) -> tuple[str, str | None, str]:
    runtime = overrides or {}
    normalized = _resolve_provider(provider)
    if normalized == "qwen":
        return (
            runtime.get("api_key") or os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY", ""),
            runtime.get("base_url") or os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
            runtime.get("model") or os.getenv("QWEN_MODEL", "qwen-plus"),
        )
    return (
        runtime.get("api_key") or os.getenv("OPENAI_API_KEY", ""),
        runtime.get("base_url") or os.getenv("OPENAI_BASE_URL"),
        runtime.get("model") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    )


def is_ai_ready(provider: str, overrides: ProviderOverrides | None = None) -> tuple[bool, str, str]:
    """Check whether selected provider, SDK and API key are available."""
    chosen_provider = _resolve_provider(provider)
    api_key, _, _ = _provider_config(chosen_provider, overrides=overrides)
    has_key = bool(api_key)
    if not has_key:
        if chosen_provider == "qwen":
            return False, "未检测到 QWEN_API_KEY / DASHSCOPE_API_KEY（请先配置后再生成）。", chosen_provider
        return False, "未检测到 OPENAI_API_KEY（请先配置后再生成）。", chosen_provider

    try:
        importlib.import_module("openai")
    except ModuleNotFoundError:
        return False, "未安装 openai SDK，请先安装 requirements.txt 依赖。", chosen_provider

    return True, f"已启用大模型增强输出（{chosen_provider.upper()}）。", chosen_provider




def _extract_error_code(exc: Exception) -> str:
    """Extract provider error code from OpenAI-compatible exceptions."""
    code = getattr(exc, "code", None)
    if isinstance(code, str) and code.strip():
        return code.strip()

    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        nested_code = body.get("code")
        if isinstance(nested_code, str) and nested_code.strip():
            return nested_code.strip()
        error_payload = body.get("error")
        if isinstance(error_payload, dict):
            nested_code = error_payload.get("code")
            if isinstance(nested_code, str) and nested_code.strip():
                return nested_code.strip()

    response = getattr(exc, "response", None)
    if response is not None:
        try:
            payload: Any = response.json()
        except Exception:  # noqa: BLE001
            payload = None
        if isinstance(payload, dict):
            nested_code = payload.get("code")
            if isinstance(nested_code, str) and nested_code.strip():
                return nested_code.strip()
            error_payload = payload.get("error")
            if isinstance(error_payload, dict):
                nested_code = error_payload.get("code")
                if isinstance(nested_code, str) and nested_code.strip():
                    return nested_code.strip()

    return ""


def _is_recoverable_openai_access_error(exc: Exception) -> bool:
    """Whether an OpenAI failure should fallback to another provider."""
    code = _extract_error_code(exc).lower()
    if not code:
        return False
    return code in {"accessdenied.unpurchased", "invalid_api_key", "insufficient_quota"}

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


def enhance_plan_with_ai(
    spec: ResearchSpec,
    sections: list[PlanSection],
    provider: str,
    overrides: ProviderOverrides | None = None,
) -> dict | None:
    """Return AI-enhanced plan payload, or None when API output is invalid."""
    ready, _, chosen_provider = is_ai_ready(provider, overrides=overrides)
    if not ready:
        return None

    def _request_with_provider(target_provider: str) -> dict | None:
        api_key, base_url, model = _provider_config(target_provider, overrides=overrides)
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

    openai_module = importlib.import_module("openai")
    auth_error_type = getattr(openai_module, "AuthenticationError", None)

    if chosen_provider != "openai":
        try:
            return _request_with_provider(chosen_provider)
        except Exception as exc:  # noqa: BLE001
            provider_name = chosen_provider.upper()
            raise RuntimeError(
                f"{provider_name} 请求失败，请检查 API Key、账户权限、模型名称或 Base URL 配置。"
            ) from exc

    try:
        return _request_with_provider("openai")
    except Exception as exc:  # noqa: BLE001
        has_qwen_key = bool(os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY"))
        should_fallback = bool(auth_error_type and isinstance(exc, auth_error_type))
        if not should_fallback:
            should_fallback = _is_recoverable_openai_access_error(exc)

        if should_fallback and has_qwen_key:
            return _request_with_provider("qwen")

        error_code = _extract_error_code(exc)
        hint = "（可尝试切换到 Qwen）"
        if error_code:
            hint = f"（错误码: {error_code}，可尝试切换到 Qwen）"
        raise RuntimeError(
            f"OpenAI 请求失败，请检查 API Key、账户权限或模型可用性{hint}。"
        ) from exc
