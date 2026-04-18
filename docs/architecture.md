# ResearchToolAgent 架构说明

## 1. 系统模块说明

- **app.py（UI 编排层）**
  - 使用 Streamlit 提供输入表单与多标签输出页面。
  - 将解析、规划、可视化、GitHub 发布建议、创新点统一编排到同一视图。

- **core/schemas.py（数据模型层）**
  - 使用 Pydantic 定义 `ResearchSpec`、`PlanSection`、`ScaffoldSuggestion` 等数据契约。

- **core/parser.py（需求解析层）**
  - 通过关键词与显式输入推断任务类型、输入输出格式、部署形态。

- **core/planner.py（规划与模板层）**
  - 生成总览、分阶段执行计划、项目骨架与初始化文件模板。

- **core/ai_planner.py（大模型增强层）**
  - 调用 OpenAI 兼容 API（OpenAI/Qwen）增强方案文案和协作建议。

- **core/diagram.py（流程图层）**
  - 生成美化版 Mermaid 主流程图与文字解释。

- **core/explain.py（可解释性层）**
  - 输出工具核心算法分步逻辑。
  - 输出 API 职责地图与时序图，帮助团队理解每个接口作用。

- **core/github_publish.py（发布建议层）**
  - 生成“直接调用 GitHub API 创建仓库 + push 代码”的可复制脚本。

- **core/advisor.py（人性化建议层）**
  - 提供可行性体检（评分+建议）与分阶段行动清单（Today/This Week/Next Stage）。

- **core/humanize.py（交互增强层）**
  - 生成用户视角故事与智能追问列表，帮助补齐需求空白。

- **core/innovation.py（创新点层）**
  - 输出可落地创新点建议，用于后续迭代规划。

## 2. 请求处理流程

1. 用户提交自然语言需求和可选参数。
2. `parser` 将输入标准化为 `ResearchSpec`。
3. `planner` 生成概览、阶段计划、项目骨架、初始化文件。
4. （可选）`ai_planner` 增强文案并补充协作动作。
5. `explain` 输出核心算法步骤、API 职责说明、时序图。
6. `diagram` 输出主流程图和解释。
7. `github_publish` 输出直接发布到 GitHub 的脚本与步骤。
8. `advisor` 输出可行性体检与行动清单，提升落地节奏感。
9. `humanize` 输出用户故事与智能追问，降低沟通歧义。
10. UI 汇总输出完整研发包。

## 3. 为什么这种架构适合 MVP

- **模块职责清晰**：解析、规划、可视化、发布建议互相独立，方便迭代。
- **落地效率高**：不仅生成方案，还包含初始化文件与发布脚本。
- **可解释性增强**：新增算法逻辑拆解与 API 职责地图，降低团队对黑盒的担忧。

## 4. 后续扩展方向

- 增加真实 GitHub OAuth 授权与一键发布按钮（后端代理安全存储 Token）
- 支持流程图可视化渲染（Mermaid 直接渲染而非仅源码展示）
- 增加 API 调用链路指标（耗时、失败率、回退率）
- 引入模板插件机制，面向不同科研子领域提供专用策略
