"""Planner module for creating actionable project plans."""

from __future__ import annotations

from core.schemas import PlanSection, ResearchSpec, ScaffoldEntry, ScaffoldSuggestion


def build_overview(spec: ResearchSpec) -> str:
    """Generate concise overview from structured spec."""
    training_note = "包含模型训练闭环" if spec.needs_training else "以规则/算法流程为主"
    if spec.github_sync:
        repo_ref = f"{spec.github_owner}/{spec.github_repo}" if spec.github_owner and spec.github_repo else "目标仓库待补充"
        github_note = f"已启用 GitHub 协作同步（目标：{repo_ref}）"
    else:
        github_note = "当前为本地优先方案"
    deliverables_text = "、".join(spec.deliverables)
    return (
        f"### {spec.project_name}\n"
        f"我理解你要做的是一个 **{spec.task_type}**，核心目标是：{spec.problem_statement}\n\n"
        f"- 输入数据：{spec.input_format}\n"
        f"- 输出目标：{spec.output_format}\n"
        f"- 部署形态：{spec.deployment_form}\n"
        f"- 实施特点：{training_note}，{github_note}，并产出 {deliverables_text}。"
    )


def build_design_plan(spec: ResearchSpec) -> list[PlanSection]:
    """Generate five-step design plan tailored for research tooling."""
    if spec.needs_training:
        sections = [
            PlanSection(
                title="阶段 1：数据契约与实验边界",
                items=[
                    f"明确输入数据规范：{spec.input_format}，定义样本粒度、标签字典与数据切分策略。",
                    "建立数据质控清单（缺失值、异常值、类别分布、重复样本）并输出 QC 报告。",
                    "定义首版验收目标：至少一个核心指标（如 F1）+ 一个稳定性指标（如方差/置信区间）。",
                ],
            ),
            PlanSection(
                title="阶段 2：Baseline 与可复现训练",
                items=[
                    "先实现可复现 baseline（固定随机种子、固定切分、固定评估脚本）。",
                    "将训练参数配置化（学习率、batch size、epoch、正则化策略）。",
                    "记录训练日志与模型版本，确保同一配置可重复得到一致结果。",
                ],
            ),
            PlanSection(
                title="阶段 3：评估体系与误差分析",
                items=[
                    f"围绕 {spec.output_format} 设计评估输出：指标表、混淆矩阵、关键样本误差分析。",
                    "补充分组评估（按类别/样本来源）定位模型失效边界。",
                    "沉淀误差修复策略：数据增强、特征修正、阈值调优。",
                ],
            ),
            PlanSection(
                title="阶段 4：可解释性与报告自动化",
                items=[
                    "输出可解释性结果（特征重要性/SHAP）并形成可读结论。",
                    "自动生成评估报告（结论摘要、图表、配置快照、复现实验命令）。",
                    "将报告结构模板化，保证每轮迭代都可横向对比。",
                ],
            ),
            PlanSection(
                title="阶段 5：工程化交付与协作",
                items=[
                    "封装训练入口脚本（CLI）并统一产物目录（模型、日志、图表、报告）。",
                    "建立单元测试与回归测试，覆盖数据解析和评估逻辑。",
                    "形成版本化交付规范（版本号、变更记录、回滚策略）。",
                ],
            ),
        ]
        if spec.github_sync:
            sections[4].items.append("采用 GitHub Flow + PR 审阅 + CI 校验，保证多人协作质量。")
        return sections

    sections = [
        PlanSection(
            title="阶段 1：输入与数据约定",
            items=[
                f"定义输入格式与字段映射：{spec.input_format}",
                "提供最小可运行样例数据与数据校验规则，确保复现实验。",
                "补充异常数据处理策略（缺失值、格式错误、样本长度不一致）。",
            ],
        ),
        PlanSection(
            title="阶段 2：任务拆解与里程碑",
            items=[
                "将需求拆分为：解析层、核心算法层、结果组织层、展示层。",
                "每个子模块提供独立函数接口，便于单元测试与后续替换。",
                "在 docs 中维护流程说明与里程碑，支持科研协作与审阅。",
            ],
        ),
        PlanSection(
            title="阶段 3：核心算法模块",
            items=[
                f"围绕 {spec.task_type} 构建可插拔算法流程。",
                "预留参数配置入口，支持快速试验不同策略。",
                "为关键中间结果建立可追踪日志，降低调试成本。",
            ],
        ),
        PlanSection(
            title="阶段 4：输出与评估方式",
            items=[
                f"生成面向交付的输出：{spec.output_format}。",
                "定义基础评估指标（准确性、稳定性、运行效率）。",
                "将结果组织成结构化报告，便于复盘与比对。",
            ],
        ),
        PlanSection(
            title="阶段 5：可扩展与协作",
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
    if spec.github_sync:
        sections[4].items.append("采用 GitHub Flow：feature 分支开发 + PR 审阅 + CI 校验后合并。")

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


def build_bootstrap_files(spec: ResearchSpec) -> dict[str, str]:
    """Generate practical starter files for full project bootstrapping."""
    readme = (
        f"# {spec.project_name}\n\n"
        f"## 项目目标\n{spec.problem_statement}\n\n"
        "## 快速开始\n"
        "```bash\n"
        "python -m venv .venv\n"
        "source .venv/bin/activate\n"
        "pip install -r requirements.txt\n"
        "python -m src.main --help\n"
        "```\n\n"
        "## 输入输出\n"
        f"- 输入：{spec.input_format}\n"
        f"- 输出：{spec.output_format}\n\n"
        "## 研发阶段\n"
        "1. 数据准备与质控\n"
        "2. 核心算法实现\n"
        "3. 评估与报告生成\n"
    )

    pyproject = (
        "[project]\n"
        f'name = "{spec.project_name.lower()}"\n'
        'version = "0.1.0"\n'
        'description = "Research tool scaffold generated by ResearchToolAgent"\n'
        'readme = "README.md"\n'
        'requires-python = ">=3.10"\n'
        "dependencies = []\n"
    )

    main_py = (
        '"""CLI entrypoint for the generated research project."""\n\n'
        "import argparse\n\n"
        "def main() -> None:\n"
        "    parser = argparse.ArgumentParser(description='Research tool entrypoint')\n"
        "    parser.add_argument('--input', default='data/input')\n"
        "    parser.add_argument('--output', default='outputs')\n"
        "    args = parser.parse_args()\n"
        "    print(f'Input: {args.input}')\n"
        "    print(f'Output: {args.output}')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )

    files = {
        "README.md": readme,
        "pyproject.toml": pyproject,
        "src/main.py": main_py,
        ".gitignore": ".venv/\n__pycache__/\n*.pyc\noutputs/\n.env\n",
    }

    if spec.github_sync:
        files[".github/workflows/ci.yml"] = (
            "name: CI\n\n"
            "on:\n  push:\n  pull_request:\n\n"
            "jobs:\n"
            "  test:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "      - uses: actions/setup-python@v5\n"
            "        with:\n"
            "          python-version: '3.11'\n"
            "      - run: python -m pip install --upgrade pip\n"
            "      - run: if [ -f requirements.txt ]; then pip install -r requirements.txt; fi\n"
            "      - run: python -m compileall src || true\n"
        )
        files[".github/ISSUE_TEMPLATE/feature_request.md"] = (
            "---\nname: 功能需求\nabout: 新功能提案\n---\n\n"
            "## 背景\n\n## 目标\n\n## 验收标准\n- [ ]\n"
        )
        files[".github/pull_request_template.md"] = (
            "## 变更说明\n\n## 测试说明\n\n## 风险与回滚\n"
        )

    return files
