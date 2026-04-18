"""Mermaid flowchart generation utilities."""

from __future__ import annotations


def generate_mermaid_flow(task_type: str) -> str:
    """Generate a cleaner Mermaid flowchart for planning workflow."""
    branch = "训练规划" if task_type == "深度学习模型工具" else "算法规划"
    return f"""flowchart LR
    subgraph 输入层
        A[用户需求文本]
        B[表单参数]
    end

    subgraph 解析与路由
        C[需求解析]
        D[任务路由: {task_type}]
    end

    subgraph 规划与生成
        E[方案生成: {branch}]
        F[项目骨架生成]
        G[初始化文件生成]
    end

    subgraph 输出层
        H[流程图与文档说明]
        I[GitHub 协作动作]
        J[创新点建议]
    end

    A --> C
    B --> C
    C --> D --> E --> F --> G
    E --> H
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
        "新版流程图将链路拆成四层：输入、解析与路由、规划与生成、输出。"
        f"其中路由节点会根据任务类型切到 **{task_type}** 分支，"
        "从而影响后续方案模板与交付内容，便于团队快速定位每一步责任。"
    )
