"""Heuristic parser for converting natural language into structured specs."""

from __future__ import annotations

from core.schemas import ResearchSpec

TASK_KEYWORDS = {
    "数据清洗与质控工具": ["清洗", "质控", "去噪", "缺失值", "异常值", "qc", "预处理"],
    "信号处理工具": ["signal", "信号", "chunk", "denoise", "normalize", "滤波"],
    "序列分析工具": ["序列", "fasta", "fastq", "bam", "isoform", "variant", "比对"],
    "统计建模与推断工具": ["统计", "回归", "检验", "bayes", "bootstrap", "置信区间"],
    "深度学习模型工具": ["训练", "模型", "分类", "预测", "deep learning", "神经网络"],
    "可视化与报告工具": ["可视化", "图表", "dashboard", "plot", "报告"],
    "流程编排/CLI 工具": ["pipeline", "workflow", "cli", "命令行", "流程", "编排"],
    "网页应用工具": ["网页", "web", "streamlit", "flask", "前端"],
    "多智能体/自动化科研助理": ["agent", "智能体", "自动化", "assistant", "copilot", "工作流助手"],
}

INPUT_HINTS = ["npy", "csv", "jsonl", "bam", "fastq", "fasta", "txt", "parquet"]
OUTPUT_HINTS = ["报告", "图", "可视化", "表格", "metrics", "模型", "预测", "json"]


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def infer_task_type(user_text: str, selected_task: str | None) -> str:
    """Infer task category from explicit selection or keyword matching."""
    if selected_task and selected_task != "自动识别（推荐）":
        return selected_task
    lowered = user_text.lower()
    best_task = None
    best_score = 0
    for task, keywords in TASK_KEYWORDS.items():
        score = sum(1 for word in keywords if word.lower() in lowered)
        if score > best_score:
            best_score = score
            best_task = task
    if best_task:
        return best_task
    return "通用科研分析工具"


def infer_input_format(user_text: str, input_format: str | None) -> str:
    """Infer input format with precedence to explicit form input."""
    if input_format:
        return input_format
    lowered = user_text.lower()
    hits = [hint for hint in INPUT_HINTS if hint in lowered]
    return ", ".join(hits) if hits else "待定义（建议在规格中补充数据模式）"


def infer_output_format(user_text: str, output_format: str | None) -> str:
    """Infer output targets based on demand description."""
    if output_format:
        return output_format
    lowered = user_text.lower()
    hits = [hint for hint in OUTPUT_HINTS if hint.lower() in lowered]
    if hits:
        return ", ".join(dict.fromkeys(hits))
    return "结构化结果 + 可复用文档"


def infer_training(user_text: str, checkbox: bool) -> bool:
    """Decide whether model training is required."""
    if checkbox:
        return True
    lowered = user_text.lower()
    trigger_words = ["训练", "train", "分类", "预测", "model"]
    return _contains_any(lowered, trigger_words)


def infer_deployment_form(user_text: str, task_type: str) -> str:
    """Infer deployment style from request and task category."""
    lowered = user_text.lower()
    if _contains_any(lowered, ["网页", "web", "streamlit", "dashboard"]) or task_type == "网页应用工具":
        return "web app"
    if _contains_any(lowered, ["cli", "命令行", "pipeline", "workflow"]):
        return "cli"
    if task_type in {"信号处理工具", "序列分析工具", "流程编排/CLI 工具", "数据清洗与质控工具"}:
        return "python package + scripts"
    return "python library"


def build_deliverables(task_type: str, needs_training: bool, wants_github: bool) -> list[str]:
    """Build default deliverables list according to parsed intent."""
    deliverables = ["结构化需求说明", "可执行设计方案", "推荐项目骨架", "Mermaid 逻辑图"]
    if task_type in {"可视化与报告工具", "网页应用工具"}:
        deliverables.append("可视化界面原型说明")
    if needs_training:
        deliverables.extend(["训练与评估流程定义", "实验配置建议"])
    if wants_github:
        deliverables.extend(["GitHub 仓库初始化命令", "分支与协作规范建议", "CI 校验建议"])
    return deliverables


def parse_user_request(
    project_name: str,
    problem_statement: str,
    task_type: str,
    input_format: str,
    output_format: str,
    needs_training: bool,
    github_sync: bool,
) -> ResearchSpec:
    """Parse UI inputs into a normalized structured specification."""
    inferred_task = infer_task_type(problem_statement, task_type)
    inferred_training = infer_training(problem_statement, needs_training)

    return ResearchSpec(
        project_name=project_name.strip() or "UntitledResearchTool",
        problem_statement=problem_statement.strip(),
        task_type=inferred_task,
        input_format=infer_input_format(problem_statement, input_format.strip() or None),
        output_format=infer_output_format(problem_statement, output_format.strip() or None),
        needs_training=inferred_training,
        deployment_form=infer_deployment_form(problem_statement, inferred_task),
        github_sync=github_sync,
        deliverables=build_deliverables(inferred_task, inferred_training, github_sync),
    )
