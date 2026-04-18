"""Mermaid flowchart generation utilities."""

from __future__ import annotations


def generate_mermaid_flow(task_type: str) -> str:
    """Generate a project implementation flowchart for the user's requested tool."""
    branch = "训练规划" if task_type == "深度学习模型工具" else "算法规划"
    return f"""flowchart LR
    subgraph 数据输入
        A[多文件数据输入]
        B[数据格式校验]
    end

    subgraph 数据处理与建模
        C[预处理与特征工程]
        D[{branch}]
        E[模型训练与调参]
    end

    subgraph 评估与解释
        F[模型评估指标]
        G[可解释性分析]
    end

    subgraph 交付输出
        H[评估报告]
        I[可视化图表]
        J[模型与日志导出]
    end

    A --> B --> C --> D --> E --> F --> G
    F --> H
    G --> I
    E --> J

    classDef input fill:#E8F4FF,stroke:#4A90E2,color:#0D2B45;
    classDef core fill:#EAFCEF,stroke:#34A853,color:#1B4332;
    classDef out fill:#FFF4E6,stroke:#F2994A,color:#7A3E00;

    class A,B input;
    class C,D,E,F,G core;
    class H,I,J out;
"""


def build_diagram_explanation(task_type: str) -> str:
    """Provide human-readable explanation for diagram."""
    return (
        "流程图聚焦你要开发的业务工具本身：从数据输入开始，经过预处理、建模、评估与解释，"
        f"再输出报告与图表。中间会根据任务类型切到 **{task_type}** 的策略分支，"
        "确保不是在解释平台内部实现，而是在描述你项目的落地流程。"
    )
