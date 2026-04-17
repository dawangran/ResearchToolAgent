# ResearchToolAgent 架构说明

## 1. 系统模块说明

- **app.py（UI 层）**
  - 使用 Streamlit 提供输入表单与多标签输出视图。
  - 协调 parser、planner、diagram、innovation 等模块并展示结果。

- **core/schemas.py（数据模型层）**
  - 使用 Pydantic 定义结构化需求与规划输出模型。
  - 为模块间交互提供统一且可验证的数据契约。

- **core/parser.py（需求解析层）**
  - 通过关键词、规则与启发式逻辑进行任务分类与字段推断。
  - 自动补全输入格式、输出目标、部署形式等字段。

- **core/planner.py（方案规划层）**
  - 依据任务类型与需求特征生成任务概述、分步骤设计方案和项目骨架。
  - 生成可直接落地的初始化文件模板（README、pyproject、CLI 入口、GitHub CI/模板）。

- **core/ai_planner.py（可选大模型增强层）**
  - 在配置 `OPENAI_API_KEY` 或 `QWEN_API_KEY` 且用户启用时，调用 OpenAI 兼容 API 对方案文案进行增强。
  - 输出更人性化的概览、阶段计划，以及补充的 GitHub 协作动作。

- **core/diagram.py（流程图层）**
  - 生成 Mermaid flowchart 源码，表达需求到交付的主流程。

- **core/innovation.py（创新点层）**
  - 从方法、工程、交互、领域应用等维度输出具体创新点。

## 2. 请求处理流程

1. 用户在网页填写需求描述及可选字段。
2. `parser` 将输入转化为 `ResearchSpec`。
3. `planner` 根据结构化规格生成概览、设计方案和骨架。
4. （可选）`ai_planner` 对概览/计划进行大模型增强。
5. `diagram` 生成流程图代码与解释。
6. `innovation` 输出创新点。
7. UI 通过 tabs 呈现完整研发包，并展示可复制的项目初始化文件内容。

## 3. 为什么这种架构适合 MVP

- **简单且完整**：无数据库，模型调用统一走 OpenAI 兼容 API（OpenAI/Qwen），部署路径清晰。
- **模块边界清晰**：每个功能单元职责单一，方便测试与迭代。
- **可扩展性好**：未来可替换 parser 为更强模型，或增加导出/协作模块而不破坏现有结构。

## 4. 后续扩展方向

- 增加配置驱动规则（YAML/JSON）
- 引入模板版本管理与项目类型插件机制
- 加入实验追踪与自动报告
- 逐步接入 LLM 以提升复杂语义解析能力
