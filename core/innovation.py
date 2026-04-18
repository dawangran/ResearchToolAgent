"""Innovation point generation for research tool planning."""

from __future__ import annotations

from core.schemas import ResearchSpec


def generate_innovation_points(spec: ResearchSpec) -> list[str]:
    """Generate concrete innovation points across multiple dimensions."""
    points = [
        f"【方法创新】围绕“{spec.problem_statement[:24]}...”设计可复现的端到端 pipeline：数据读取→建模→评估→解释→交付。",
        "【工程创新】将训练配置、随机种子与数据切分策略显式化，保证实验可复现与结果可追踪。",
        f"【产品创新】交付物直接对齐业务目标（{spec.output_format}），减少‘模型有了但无法汇报/复盘’的问题。",
    ]

    if spec.task_type in {"序列分析工具", "信号处理工具", "深度学习模型工具"}:
        points.append(
            "【领域应用创新】针对科研常见数据（如 FASTQ/BAM/NPY）提供统一的数据质控与特征处理策略，加速落地。"
        )

    if spec.needs_training:
        points.append(
            "【可解释训练创新】把模型可解释性纳入默认输出（特征重要性/SHAP），让性能提升与科学解释同步推进。"
        )

    return points[:5]
