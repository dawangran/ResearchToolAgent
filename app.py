"""Streamlit entrypoint for ResearchToolAgent MVP."""

from __future__ import annotations

import streamlit as st

from core.ai_planner import enhance_plan_with_ai, is_ai_ready
from core.diagram import build_diagram_explanation, generate_mermaid_flow
from core.innovation import generate_innovation_points
from core.parser import parse_user_request
from core.planner import build_bootstrap_files, build_design_plan, build_overview, build_project_scaffold


EXAMPLE_PROMPT = (
    "开发一个训练脚本，输入多个 npy 文件，输出一个可解释的分类模型，并自动生成评估报告和可视化图表。"
)


def _render_header() -> None:
    st.title("ResearchToolAgent")
    st.caption("像 AI 产品经理一样，把你的想法转化为可落地研发方案 + GitHub 协作动作")


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
            options=[
                "",
                "自动识别（推荐）",
                "数据清洗与质控工具",
                "信号处理工具",
                "序列分析工具",
                "统计建模与推断工具",
                "深度学习模型工具",
                "可视化与报告工具",
                "流程编排/CLI 工具",
                "网页应用工具",
                "多智能体/自动化科研助理",
                "通用科研分析工具",
            ],
            help="如果不确定，建议选择“自动识别（推荐）”，系统会结合你的描述自动判断。",
        )
        input_type = st.text_input("输入数据类型（可选）", placeholder="例如：npy, fastq, csv")
        output_goal = st.text_input("输出目标（可选）", placeholder="例如：分类结果 + 报告 + 图表")
        needs_training = st.checkbox("是否需要训练模型（可选）", value=False)
        github_sync = st.checkbox("是否需要 GitHub 同步（可选）", value=True)
        ai_provider = st.selectbox(
            "大模型提供方（必选）",
            options=["自动", "OpenAI", "Qwen"],
            index=0,
            help="仅支持 OpenAI/Qwen；自动模式优先尝试 OPENAI_API_KEY，其次 QWEN_API_KEY。",
        )
        submitted = st.form_submit_button("生成（仅大模型）方案包", type="primary")

    return {
        "submitted": submitted,
        "project_name": project_name,
        "problem_statement": problem_statement,
        "task_type": task_type,
        "input_type": input_type,
        "output_goal": output_goal,
        "needs_training": needs_training,
        "github_sync": github_sync,
        "ai_provider": ai_provider,
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
    bootstrap_files = build_bootstrap_files(spec)
    mermaid_code = generate_mermaid_flow(spec.task_type)
    diagram_note = build_diagram_explanation(spec.task_type)
    innovation_points = generate_innovation_points(spec)
    github_actions_from_ai: list[str] = []

    ready, ai_message, chosen_provider = is_ai_ready(inputs["ai_provider"])
    if not ready:
        st.error(ai_message)
        st.stop()

    ai_payload = enhance_plan_with_ai(spec, design_plan, chosen_provider)
    if not ai_payload:
        st.error("大模型返回结果不可解析，请重试或更换模型。")
        st.stop()

    overview = str(ai_payload.get("overview_md", overview))
    ai_sections = ai_payload.get("sections", [])
    if isinstance(ai_sections, list):
        parsed_sections = []
        for section in ai_sections:
            if isinstance(section, dict) and section.get("title") and isinstance(section.get("items"), list):
                parsed_sections.append(section)
        if parsed_sections:
            design_plan = parsed_sections
    ai_actions = ai_payload.get("github_actions", [])
    if isinstance(ai_actions, list):
        github_actions_from_ai = [str(action) for action in ai_actions if str(action).strip()]
    st.success(ai_message)

    tabs = st.tabs(
        [
            "AI 总览",
            "结构化需求",
            "分阶段执行方案",
            "项目骨架",
            "初始化文件",
            "逻辑图",
            "GitHub 协作",
            "创新点",
        ]
    )

    with tabs[0]:
        st.markdown(overview)

    with tabs[1]:
        st.json(spec.model_dump())

    with tabs[2]:
        for idx, section in enumerate(design_plan, start=1):
            if isinstance(section, dict):
                title = section.get("title", f"阶段 {idx}")
                items = section.get("items", [])
            else:
                title = section.title
                items = section.items
            st.markdown(f"**{idx}. {title}**")
            for bullet in items:
                st.markdown(f"- {bullet}")

    with tabs[3]:
        st.code(scaffold.tree, language="text")
        for item in scaffold.descriptions:
            st.markdown(f"- **{item.path}**：{item.purpose}")

    with tabs[4]:
        st.markdown("以下内容可直接复制到项目中，快速完成初始化：")
        for path, content in bootstrap_files.items():
            st.markdown(f"**{path}**")
            language = "yaml" if path.endswith((".yml", ".yaml")) else "markdown" if path.endswith(".md") else "toml" if path.endswith(".toml") else "python" if path.endswith(".py") else "text"
            st.code(content, language=language)

    with tabs[5]:
        st.code(mermaid_code, language="mermaid")
        st.markdown(diagram_note)

    with tabs[6]:
        if spec.github_sync:
            st.markdown(
                """
                ### 推荐 GitHub 同步动作
                1. 初始化仓库并创建 `main` + `dev` 双分支策略。  
                2. 在 `README.md` 写清目标、运行方式、数据入口与输出说明。  
                3. 建立 issue 模板（需求、bug、实验记录）与 PR 模板。  
                4. 配置基础 CI（lint + test + build）确保每次合并可验证。  
                5. 使用里程碑管理研究阶段（MVP、实验优化、可复现发布）。  
                """
            )
            st.code(
                "\n".join(
                    [
                        "git init",
                        "git checkout -b main",
                        "git checkout -b dev",
                        "git add .",
                        "git commit -m 'chore: bootstrap project scaffold'",
                        "git remote add origin <your-repo-url>",
                        "git push -u origin main",
                        "git push -u origin dev",
                    ]
                ),
                language="bash",
            )
            if github_actions_from_ai:
                st.markdown("### AI 补充协作建议")
                for action in github_actions_from_ai:
                    st.markdown(f"- {action}")
        else:
            st.info("你当前未勾选 GitHub 同步；若需要团队协作，建议启用后自动生成同步动作。")

    with tabs[7]:
        for idx, point in enumerate(innovation_points, start=1):
            st.markdown(f"{idx}. {point}")


if __name__ == "__main__":
    main()
