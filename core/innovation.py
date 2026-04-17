"""Innovation point generation for research tool planning."""

from __future__ import annotations

from core.schemas import ResearchSpec


def generate_innovation_points(spec: ResearchSpec) -> list[str]:
    """Generate concrete innovation points across multiple dimensions."""
    points = [
        f"【方法创新】针对“{spec.problem_statement[:24]}...”构建任务模板化解析规则，降低科研需求到可执行方案的转换门槛。",
        "【工程创新】采用 Pydantic 结构化规格，保证字段完整性与类型一致性，便于后续接入自动测试与配置驱动开发。",
        f"【产品/交互创新】通过一次输入同步产出概览、设计方案、目录骨架和 Mermaid 图，减少跨文档沟通成本，提升需求评审效率。",
    ]

    if spec.task_type in {"序列分析工具", "信号处理工具", "深度学习模型工具"}:
        points.append(
            "【领域应用创新】将科研常见输入格式识别（如 FASTQ/BAM/NPY）内置到解析流程，支持生信与算法研发场景的快速落地。"
        )

    if spec.needs_training:
        points.append(
            "【方法+工程协同创新】在 MVP 阶段即预置训练与评估闭环建议，可直接衔接实验追踪和模型迭代流程。"
        )

    return points[:5]
