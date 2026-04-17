"""Planner module for creating actionable project plans."""

from __future__ import annotations

from core.schemas import PlanSection, ResearchSpec, ScaffoldEntry, ScaffoldSuggestion


def build_overview(spec: ResearchSpec) -> str:
    """Generate concise overview from structured spec."""
    training_note = "包含模型训练闭环" if spec.needs_training else "以规则/算法流程为主"
    deliverables_text = "、".join(spec.deliverables)
    return (
        f"### {spec.project_name}\n"
        f"该工具属于 **{spec.task_type}**，目标是解决：{spec.problem_statement}\n\n"
        f"- 输入数据：{spec.input_format}\n"
        f"- 输出目标：{spec.output_format}\n"
        f"- 部署形态：{spec.deployment_form}\n"
        f"- 实施特点：{training_note}，并产出 {deliverables_text}。"
    )


def build_design_plan(spec: ResearchSpec) -> list[PlanSection]:
    """Generate five-step design plan tailored for research tooling."""
    sections = [
        PlanSection(
            title="输入与数据约定",
            items=[
                f"定义输入格式与字段映射：{spec.input_format}",
                "提供最小可运行样例数据与数据校验规则，确保复现实验。",
                "补充异常数据处理策略（缺失值、格式错误、样本长度不一致）。",
            ],
        ),
        PlanSection(
            title="任务拆解",
            items=[
                "将需求拆分为：解析层、核心算法层、结果组织层、展示层。",
                "每个子模块提供独立函数接口，便于单元测试与后续替换。",
                "在 docs 中维护流程说明，支持科研协作与审阅。",
            ],
        ),
        PlanSection(
            title="核心算法模块",
            items=[
                f"围绕 {spec.task_type} 构建可插拔算法流程。",
                "预留参数配置入口，支持快速试验不同策略。",
                "为关键中间结果建立可追踪日志，降低调试成本。",
            ],
        ),
        PlanSection(
            title="输出与评估方式",
            items=[
                f"生成面向交付的输出：{spec.output_format}。",
                "定义基础评估指标（准确性、稳定性、运行效率）。",
                "将结果组织成结构化报告，便于复盘与比对。",
            ],
        ),
        PlanSection(
            title="可扩展点",
            items=[
                "支持新数据格式与新任务模板的快速接入。",
                "逐步引入自动化测试与基准数据集回归验证。",
                "可扩展到多用户协作场景（版本管理、任务模板库）。",
            ],
        ),
    ]

    if spec.needs_training:
        sections[2].items.append("加入训练/验证/测试分层流程及模型持久化策略。")
        sections[3].items.append("增加模型评估指标（AUC、F1、混淆矩阵）与阈值分析。")

    return sections


def build_project_scaffold(spec: ResearchSpec) -> ScaffoldSuggestion:
    """Return recommended project tree and directory purposes."""
    if spec.task_type == "网页应用工具":
        tree = (
            f"{spec.project_name}/\n"
            "├── app.py\n"
            "├── core/\n"
            "├── docs/\n"
            "├── tests/\n"
            "└── README.md"
        )
        desc = [
            ScaffoldEntry(path="app.py", purpose="Web 入口与交互层。"),
            ScaffoldEntry(path="core/", purpose="解析、规划、图与创新点等业务逻辑。"),
            ScaffoldEntry(path="docs/", purpose="架构与使用文档。"),
            ScaffoldEntry(path="tests/", purpose="核心逻辑单元测试。"),
            ScaffoldEntry(path="README.md", purpose="项目说明、运行方式与示例。"),
        ]
        return ScaffoldSuggestion(tree=tree, descriptions=desc)

    if spec.needs_training or spec.task_type == "深度学习模型工具":
        tree = (
            f"{spec.project_name}/\n"
            "├── src/\n"
            "├── configs/\n"
            "├── scripts/\n"
            "├── tests/\n"
            "├── docs/\n"
            "└── README.md"
        )
        desc = [
            ScaffoldEntry(path="src/", purpose="模型、数据处理、训练评估主代码。"),
            ScaffoldEntry(path="configs/", purpose="实验参数、数据路径、模型配置。"),
            ScaffoldEntry(path="scripts/", purpose="训练、评估、导出脚本入口。"),
            ScaffoldEntry(path="tests/", purpose="数据处理与核心算法回归测试。"),
            ScaffoldEntry(path="docs/", purpose="实验记录与方法说明。"),
            ScaffoldEntry(path="README.md", purpose="环境准备、运行命令与结果说明。"),
        ]
        return ScaffoldSuggestion(tree=tree, descriptions=desc)

    tree = (
        f"{spec.project_name}/\n"
        "├── src/\n"
        "├── scripts/\n"
        "├── docs/\n"
        "└── README.md"
    )
    desc = [
        ScaffoldEntry(path="src/", purpose="核心算法与通用工具函数。"),
        ScaffoldEntry(path="scripts/", purpose="命令行任务或批处理入口。"),
        ScaffoldEntry(path="docs/", purpose="流程说明与案例文档。"),
        ScaffoldEntry(path="README.md", purpose="快速开始与参数说明。"),
    ]
    return ScaffoldSuggestion(tree=tree, descriptions=desc)
