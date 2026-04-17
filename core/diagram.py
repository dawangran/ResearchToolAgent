"""Mermaid flowchart generation utilities."""

from __future__ import annotations


def generate_mermaid_flow(task_type: str) -> str:
    """Generate a Mermaid flowchart for planning workflow."""
    branch = "训练规划" if task_type == "深度学习模型工具" else "算法规划"
    return f"""flowchart TD
    A[用户需求] --> B[需求解析]
    B --> C[任务路由: {task_type}]
    C --> D[方案生成: {branch}]
    D --> E[代码骨架生成]
    E --> F[文档/流程图/创新点输出]
"""


def build_diagram_explanation(task_type: str) -> str:
    """Provide human-readable explanation for diagram."""
    return (
        f"该流程图展示了从自然语言需求到研发包输出的主链路："
        f"系统先解析需求，再将任务路由到 **{task_type}** 对应策略，"
        "随后生成可执行方案、推荐代码结构，并统一输出文档、流程图与创新点。"
    )
