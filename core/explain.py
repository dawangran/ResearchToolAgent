"""Explainability helpers for algorithm logic and API responsibilities."""

from __future__ import annotations

from core.schemas import ResearchSpec


def build_algorithm_logic(spec: ResearchSpec) -> list[dict[str, str]]:
    """Return concrete algorithm pipeline steps for the current request."""
    training_mode = "训练闭环" if spec.needs_training else "规则/算法闭环"
    return [
        {
            "step": "Step 1 · 结构化解析",
            "logic": "将自然语言需求转换为结构化字段（任务类型、输入/输出、部署方式、交付物）。",
            "input": "项目名称 + 需求文本 + 可选开关",
            "output": "ResearchSpec（标准化规格对象）",
        },
        {
            "step": "Step 2 · 任务路由",
            "logic": f"基于关键词匹配与显式选择进行路由，定位到 {spec.task_type} 策略模板。",
            "input": "ResearchSpec.task_type + 需求文本",
            "output": "选中的策略分支与默认阶段模板",
        },
        {
            "step": "Step 3 · 核心规划",
            "logic": f"围绕{training_mode}构建分阶段行动项：数据约定 → 算法模块 → 评估输出 → 协作发布。",
            "input": "结构化规格 + 模板规则",
            "output": "可执行计划（PlanSection 列表）",
        },
        {
            "step": "Step 4 · 工程化产物",
            "logic": "生成项目骨架与初始化文件（README、pyproject、main.py、CI 模板）。",
            "input": "结构化规格 + GitHub 同步开关",
            "output": "ScaffoldSuggestion + bootstrap files",
        },
        {
            "step": "Step 5 · 可解释输出",
            "logic": "输出流程图、API 职责说明、创新点，确保团队知道每个模块做什么与为什么做。",
            "input": "前序规划产物",
            "output": "Mermaid 图 + API 地图 + 创新点",
        },
    ]


def build_api_map() -> list[dict[str, str]]:
    """Describe what each API/module does in the pipeline."""
    return [
        {"api": "parse_user_request", "layer": "解析层", "purpose": "把自然语言与表单字段规整为 ResearchSpec 数据契约。"},
        {"api": "build_overview", "layer": "规划层", "purpose": "生成任务总览，明确目标、输入输出、部署形态和交付范围。"},
        {"api": "build_design_plan", "layer": "规划层", "purpose": "产出可执行的阶段计划与关键行动项，支持按阶段推进。"},
        {"api": "build_project_scaffold", "layer": "工程层", "purpose": "根据任务类型推荐项目目录结构和每个目录职责。"},
        {"api": "build_bootstrap_files", "layer": "工程层", "purpose": "自动产出初始化文件内容，减少从 0 到 1 的搭建时间。"},
        {"api": "enhance_plan_with_ai", "layer": "增强层", "purpose": "调用 LLM 优化方案表达，补充协作动作与可执行建议。"},
        {"api": "generate_mermaid_flow", "layer": "可视化层", "purpose": "生成研发链路流程图源码，便于展示系统主流程。"},
        {"api": "build_diagram_explanation", "layer": "可视化层", "purpose": "将流程图转换为可读说明，降低理解门槛。"},
        {"api": "generate_innovation_points", "layer": "创新层", "purpose": "从工程、方法与协作角度提炼可落地的创新点。"},
    ]


def build_algorithm_sequence_mermaid(spec: ResearchSpec) -> str:
    """Generate a cleaner sequence diagram for logic walkthrough."""
    return f"""sequenceDiagram
    autonumber
    participant U as 用户
    participant UI as Streamlit UI
    participant P as parser
    participant PL as planner
    participant AI as ai_planner
    participant D as diagram

    U->>UI: 提交需求与参数
    UI->>P: parse_user_request()
    P-->>UI: ResearchSpec({spec.task_type})
    UI->>PL: build_design_plan() + scaffold
    PL-->>UI: 阶段方案 + 初始化文件
    UI->>AI: enhance_plan_with_ai() (可选)
    AI-->>UI: 文案增强 + GitHub协作建议
    UI->>D: generate_mermaid_flow()
    D-->>UI: 流程图源码 + 解释
    UI-->>U: 展示研发包与发布步骤
"""
