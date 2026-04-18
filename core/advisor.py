"""Human-centric advisory helpers for turning plans into action."""

from __future__ import annotations

from core.schemas import ResearchSpec


def build_feasibility_report(spec: ResearchSpec) -> dict[str, object]:
    """Create a lightweight feasibility scorecard for the current plan."""
    dimensions: list[dict[str, object]] = []

    input_score = 5 if "待定义" not in spec.input_format else 2
    dimensions.append(
        {
            "dimension": "输入清晰度",
            "score": input_score,
            "advice": "输入数据类型明确，可直接进入数据契约定义。" if input_score >= 4 else "建议补充样例文件结构与字段约束。",
        }
    )

    output_score = 5 if spec.output_format and "结构化结果" not in spec.output_format else 3
    dimensions.append(
        {
            "dimension": "输出可验收性",
            "score": output_score,
            "advice": "输出目标清晰，容易制定验收标准。" if output_score >= 4 else "建议把输出细化为文件格式 + 指标 + 可视化产物。",
        }
    )

    eng_score = 5 if spec.github_sync else 3
    dimensions.append(
        {
            "dimension": "工程协作准备度",
            "score": eng_score,
            "advice": "已启用 GitHub 协作，适合团队推进。" if eng_score >= 4 else "建议开启 GitHub 同步并配置基础 CI。",
        }
    )

    model_score = 4 if spec.needs_training else 5
    dimensions.append(
        {
            "dimension": "研发复杂度可控性",
            "score": model_score,
            "advice": "含训练闭环，建议先做 baseline 再迭代。" if spec.needs_training else "无训练闭环，MVP 落地速度更快。",
        }
    )

    overall = round(sum(int(item["score"]) for item in dimensions) / len(dimensions), 2)
    level = "高可行" if overall >= 4.5 else "中可行" if overall >= 3.5 else "需补充定义"

    return {
        "overall_score": overall,
        "level": level,
        "dimensions": dimensions,
    }


def build_next_actions(spec: ResearchSpec) -> dict[str, list[str]]:
    """Build actionable to-do list for now / this week / next stage."""
    now = [
        "冻结最小输入样例（1~3 个文件）并写明字段含义。",
        "确定首个可验证输出（一个表格 + 一个图 + 一个日志）。",
        "初始化仓库并提交第一版 README 与目录骨架。",
    ]

    this_week = [
        "完成核心算法模块的最小闭环（可跑通，不追求最优）。",
        "补齐单元测试：至少覆盖解析层和核心算法层。",
        "输出第一版实验/评估报告，记录可复现命令。",
    ]

    next_stage = [
        "引入参数配置化与实验版本对比机制。",
        "增加异常数据与边界场景回归测试。",
        "完善协作文档：Issue 模板、PR 模板、里程碑规划。",
    ]

    if spec.needs_training:
        this_week.append("建立 train/val/test 划分与基线模型指标（如 F1/AUC）。")
        next_stage.append("引入自动化超参搜索与模型性能看板。")

    if spec.task_type == "网页应用工具":
        now.append("先画页面信息架构：输入区、结果区、日志区、错误提示区。")

    return {"now": now, "this_week": this_week, "next_stage": next_stage}


def build_experiment_backlog(spec: ResearchSpec) -> list[dict[str, str]]:
    """Generate innovation-oriented experiment backlog."""
    items = [
        {"name": "Baseline 对照实验", "goal": "建立可对比基线", "success": "得到首个可复现指标"},
        {"name": "误差分析实验", "goal": "识别主要失败模式", "success": "输出 Top3 失败原因与修复建议"},
        {"name": "性能/成本实验", "goal": "平衡速度与效果", "success": "给出至少 2 个可选配置档位"},
    ]
    if spec.needs_training:
        items.append({"name": "数据增强实验", "goal": "提升模型泛化", "success": "关键指标相对提升 >= 3%"})
    if spec.task_type == "网页应用工具":
        items.append({"name": "交互可用性实验", "goal": "减少用户操作成本", "success": "核心任务 3 步内完成"})
    return items
