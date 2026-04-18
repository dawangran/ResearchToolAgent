"""Streamlit entrypoint for ResearchToolAgent MVP."""

from __future__ import annotations

import streamlit as st

from core.ai_planner import enhance_plan_with_ai, is_ai_ready
from core.advisor import build_feasibility_report, build_next_actions
from core.diagram import build_diagram_explanation, generate_mermaid_flow
from core.explain import build_algorithm_logic, build_algorithm_sequence_mermaid, build_api_map
from core.github_publish import (
    build_github_preflight,
    build_github_publish_script,
    build_github_publish_steps,
    build_github_token_check_script,
)
from core.humanize import build_clarification_questions, build_user_story
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
        st.caption("如果开启 GitHub 同步，建议先填写连接信息，系统会生成可直接推送到指定仓库的脚本。")
        github_owner = st.text_input(
            "GitHub Owner（可选）",
            placeholder="例如：your-name 或 your-org",
            help="开启 GitHub 同步时建议必填，用于生成目标仓库地址。",
        )
        github_repo = st.text_input(
            "GitHub Repo（可选）",
            placeholder="例如：nano-signal-trainer",
            help="开启 GitHub 同步时建议必填；留空会自动使用项目名。",
        )
        github_visibility = st.selectbox(
            "仓库可见性（可选）",
            options=["public", "private"],
            index=0,
            help="若选择 private，脚本会默认创建私有仓库。",
        )
        github_default_branch = st.text_input(
            "默认分支名（可选）",
            value="main",
            help="用于首次推送分支名，例如 main 或 master。",
        )
        ai_provider = st.selectbox(
            "大模型提供方（必选）",
            options=["自动", "OpenAI", "Qwen"],
            index=0,
            help="仅支持 OpenAI/Qwen；自动模式优先尝试 OPENAI_API_KEY，其次 QWEN_API_KEY。",
        )
        ai_model = st.text_input(
            "模型名称（可选）",
            placeholder="例如：gpt-4.1-mini 或 qwen-plus",
            help="不填则使用环境变量或系统默认模型。",
        )
        ai_api_key = st.text_input(
            "API Key（可选）",
            type="password",
            help="可直接在界面填写；留空则读取环境变量。",
        )
        ai_base_url = st.text_input(
            "Base URL（可选）",
            placeholder="例如：https://dashscope.aliyuncs.com/compatible-mode/v1",
            help="通常仅在兼容模式或代理场景需要配置。",
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
        "github_owner": github_owner,
        "github_repo": github_repo,
        "github_visibility": github_visibility,
        "github_default_branch": github_default_branch,
        "ai_provider": ai_provider,
        "ai_model": ai_model,
        "ai_api_key": ai_api_key,
        "ai_base_url": ai_base_url,
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

    if inputs["github_sync"] and (
        not inputs["github_owner"].strip() or not inputs["github_repo"].strip()
    ):
        st.warning("你已开启 GitHub 同步：请先填写 GitHub Owner 与 GitHub Repo，再生成方案，这样可直接推送到指定仓库。")
        return

    spec = parse_user_request(
        project_name=inputs["project_name"],
        problem_statement=inputs["problem_statement"],
        task_type=inputs["task_type"],
        input_format=inputs["input_type"],
        output_format=inputs["output_goal"],
        needs_training=inputs["needs_training"],
        github_sync=inputs["github_sync"],
        github_owner=inputs["github_owner"],
        github_repo=inputs["github_repo"],
        github_visibility=inputs["github_visibility"],
        github_default_branch=inputs["github_default_branch"],
    )
    github_preflight = build_github_preflight(spec)
    if not github_preflight["ready"]:
        st.error("GitHub 同步预检未通过，请先修正以下问题：")
        for msg in github_preflight["errors"]:
            st.markdown(f"- {msg}")
        st.stop()

    overview = build_overview(spec)
    design_plan = build_design_plan(spec)
    scaffold = build_project_scaffold(spec)
    bootstrap_files = build_bootstrap_files(spec)
    mermaid_code = generate_mermaid_flow(spec.task_type)
    diagram_note = build_diagram_explanation(spec.task_type)
    innovation_points = generate_innovation_points(spec)
    algorithm_logic = build_algorithm_logic(spec)
    api_map = build_api_map(spec)
    sequence_mermaid = build_algorithm_sequence_mermaid(spec)
    github_publish_steps = build_github_publish_steps(spec)
    github_token_check_script = build_github_token_check_script()
    github_publish_script = build_github_publish_script(spec)
    feasibility_report = build_feasibility_report(spec)
    next_actions = build_next_actions(spec)
    clarification_questions = build_clarification_questions(spec)
    user_story = build_user_story(spec)
    github_actions_from_ai: list[str] = []

    ai_overrides = {
        "model": inputs["ai_model"].strip(),
        "api_key": inputs["ai_api_key"].strip(),
        "base_url": inputs["ai_base_url"].strip(),
    }
    ai_overrides = {key: value for key, value in ai_overrides.items() if value}

    ready, ai_message, chosen_provider = is_ai_ready(inputs["ai_provider"], overrides=ai_overrides)
    if not ready:
        st.error(ai_message)
        st.stop()

    try:
        ai_payload = enhance_plan_with_ai(spec, design_plan, chosen_provider, overrides=ai_overrides)
    except RuntimeError as exc:
        st.error(str(exc))
        st.stop()

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
            "核心算法逻辑",
            "API 职责地图",
            "逻辑图",
            "GitHub 直连发布",
            "可行性体检",
            "行动清单",
            "智能追问",
            "创新点",
        ]
    )

    with tabs[0]:
        st.markdown(overview)
        st.markdown("---")
        st.markdown("### 用户视角描述（更人性化）")
        st.markdown(user_story)

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
        st.markdown("### 工具核心算法（可落地逻辑）")
        for step in algorithm_logic:
            st.markdown(f"**{step['step']}**")
            st.markdown(f"- 逻辑：{step['logic']}")
            st.markdown(f"- 输入：{step['input']}")
            st.markdown(f"- 输出：{step['output']}")

    with tabs[6]:
        st.markdown("### 每个 API 是干什么的")
        st.table(api_map)
        st.caption("建议在重构时保持 API 输入输出稳定，便于替换内部实现而不破坏 UI。")

    with tabs[7]:
        st.markdown("### 主流程图（美化版）")
        st.code(mermaid_code, language="mermaid")
        st.markdown(diagram_note)
        st.markdown("### 时序图（看清调用关系）")
        st.code(sequence_mermaid, language="mermaid")

    with tabs[8]:
        st.markdown("### 直接发布到 GitHub（无需手动网页点创建）")
        st.markdown("#### 同步预检（专业版）")
        st.success("预检通过，可执行同步。")
        for warn in github_preflight["warnings"]:
            st.caption(f"提示：{warn}")
        for idx, item in enumerate(github_publish_steps, start=1):
            st.markdown(f"{idx}. {item}")
        st.markdown("**Step A：先校验 Token**")
        st.code(github_token_check_script, language="bash")
        st.markdown("**Step B：创建仓库并发布代码**")
        st.code(github_publish_script, language="bash")
        st.info("提示：请先在 GitHub 生成 PAT，并避免将 Token 提交到仓库。")

        if spec.github_sync and github_actions_from_ai:
            st.markdown("### AI 补充协作建议")
            for action in github_actions_from_ai:
                st.markdown(f"- {action}")

    with tabs[9]:
        st.markdown("### 项目可行性体检")
        st.metric("综合评分", f"{feasibility_report['overall_score']}/5", feasibility_report["level"])
        st.table(feasibility_report["dimensions"])

    with tabs[10]:
        st.markdown("### 建议你按这个节奏推进")
        st.markdown("**现在就做（Today）**")
        for item in next_actions["now"]:
            st.markdown(f"- {item}")
        st.markdown("**本周完成（This Week）**")
        for item in next_actions["this_week"]:
            st.markdown(f"- {item}")
        st.markdown("**下一阶段（Next Stage）**")
        for item in next_actions["next_stage"]:
            st.markdown(f"- {item}")

    with tabs[11]:
        st.markdown("### 系统智能追问（避免需求遗漏）")
        for idx, q in enumerate(clarification_questions, start=1):
            st.markdown(f"{idx}. {q}")

    with tabs[12]:
        for idx, point in enumerate(innovation_points, start=1):
            st.markdown(f"{idx}. {point}")


if __name__ == "__main__":
    main()
