"""Streamlit entrypoint for ResearchToolAgent MVP."""

from __future__ import annotations

import streamlit as st

from core.diagram import build_diagram_explanation, generate_mermaid_flow
from core.innovation import generate_innovation_points
from core.parser import parse_user_request
from core.planner import build_design_plan, build_overview, build_project_scaffold


EXAMPLE_PROMPT = (
    "开发一个训练脚本，输入多个 npy 文件，输出一个可解释的分类模型，并自动生成评估报告和可视化图表。"
)


def _render_header() -> None:
    st.title("ResearchToolAgent")
    st.caption("这是一个将自然语言工具需求转化为研发方案的网页助手")


def _render_input_form() -> dict:
    with st.form("request_form"):
        project_name = st.text_input("项目名称（可选）", placeholder="例如：NanoSignalTrainer")
        problem_statement = st.text_area(
            "自然语言需求描述（必填）",
            value=EXAMPLE_PROMPT,
            height=180,
            help="建议包含输入数据、目标输出、是否训练模型、部署形式等信息。",
        )
        task_type = st.selectbox(
            "任务类型（可选）",
            options=["", "信号处理工具", "序列分析工具", "深度学习模型工具", "可视化工具", "流程/CLI 工具", "网页应用工具", "通用科研分析工具"],
        )
        input_type = st.text_input("输入数据类型（可选）", placeholder="例如：npy, fastq, csv")
        output_goal = st.text_input("输出目标（可选）", placeholder="例如：分类结果 + 报告 + 图表")
        needs_training = st.checkbox("是否需要训练模型（可选）", value=False)
        github_sync = st.checkbox("是否需要 GitHub 同步（可选）", value=False)
        submitted = st.form_submit_button("生成方案", type="primary")

    return {
        "submitted": submitted,
        "project_name": project_name,
        "problem_statement": problem_statement,
        "task_type": task_type,
        "input_type": input_type,
        "output_goal": output_goal,
        "needs_training": needs_training,
        "github_sync": github_sync,
    }


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title="ResearchToolAgent", page_icon="🧪", layout="wide")
    _render_header()
    inputs = _render_input_form()

    if not inputs["submitted"]:
        st.info("填写需求后点击“生成方案”，可快速获得结构化研发包。")
        return

    if not inputs["problem_statement"].strip():
        st.warning("请先输入自然语言需求描述，再点击“生成方案”。")
        return

    spec = parse_user_request(
        project_name=inputs["project_name"],
        problem_statement=inputs["problem_statement"],
        task_type=inputs["task_type"],
        input_format=inputs["input_type"],
        output_format=inputs["output_goal"],
        needs_training=inputs["needs_training"],
        github_sync=inputs["github_sync"],
    )

    overview = build_overview(spec)
    design_plan = build_design_plan(spec)
    scaffold = build_project_scaffold(spec)
    mermaid_code = generate_mermaid_flow(spec.task_type)
    diagram_note = build_diagram_explanation(spec.task_type)
    innovation_points = generate_innovation_points(spec)

    tabs = st.tabs(
        [
            "概览 Overview",
            "结构化需求 Structured Spec",
            "设计方案 Design Plan",
            "项目骨架 Project Scaffold",
            "逻辑图 Logic Diagram",
            "创新点 Innovation Points",
        ]
    )

    with tabs[0]:
        st.markdown(overview)

    with tabs[1]:
        st.json(spec.model_dump())

    with tabs[2]:
        for idx, section in enumerate(design_plan, start=1):
            st.markdown(f"**{idx}. {section.title}**")
            for bullet in section.items:
                st.markdown(f"- {bullet}")

    with tabs[3]:
        st.code(scaffold.tree, language="text")
        for item in scaffold.descriptions:
            st.markdown(f"- **{item.path}**：{item.purpose}")

    with tabs[4]:
        st.code(mermaid_code, language="mermaid")
        st.markdown(diagram_note)

    with tabs[5]:
        for idx, point in enumerate(innovation_points, start=1):
            st.markdown(f"{idx}. {point}")


if __name__ == "__main__":
    main()
