"""Humanized interaction helpers for clearer decision-making."""

from __future__ import annotations

from core.schemas import ResearchSpec


def build_clarification_questions(spec: ResearchSpec) -> list[str]:
    """Generate concrete follow-up questions when spec is still ambiguous."""
    questions: list[str] = []
    if "待定义" in spec.input_format:
        questions.append("你能提供 1 个真实输入样例吗？（文件名、字段、大小）")
    if "结构化结果" in spec.output_format:
        questions.append("最终交付是报告、API 还是可视化页面？请按优先级排序。")
    if spec.needs_training:
        questions.append("你当前最关注哪个指标？（F1/AUC/召回率/推理速度）")
    if spec.deployment_form == "web app":
        questions.append("目标用户是谁？他们最常做的 3 个操作是什么？")
    if not questions:
        questions.append("当前需求已较完整，可直接进入实现阶段。")
    return questions


def build_user_story(spec: ResearchSpec) -> str:
    """Return a concise user-story style narrative for empathy-driven planning."""
    return (
        f"作为科研工具使用者，我希望通过 **{spec.task_type}** 快速把 `{spec.input_format}` 转成 "
        f"`{spec.output_format}`，并以 {spec.deployment_form} 形态稳定交付，"
        "从而减少手工处理时间并提升实验复现效率。"
    )
