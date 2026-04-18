# ResearchToolAgent

ResearchToolAgent 是一个面向科研与算法工具开发的网页 AI 助手（MVP）。
它可以将自然语言需求快速整理为“结构化研发包”，帮助研究者或工程师更快进入实现阶段。

## 为什么做这个工具

科研与算法项目经常卡在“需求不清晰、方案不成型、结构不统一”阶段。ResearchToolAgent 通过规则与模板化方法，把模糊需求转化为可执行方案，降低沟通与启动成本。

## MVP 能力

- 自然语言需求解析与字段补全
- 任务类型自动分类
- 输出结构化规格（Pydantic）
- 自动生成设计方案（分步骤）
- 自动生成推荐项目骨架与用途说明
- 自动生成可直接复制的初始化文件（`README.md`、`pyproject.toml`、`src/main.py`、`.gitignore`）
- 自动生成 Mermaid 逻辑流程图
- 自动生成核心算法逻辑拆解、API 职责地图与时序图
- 自动生成可行性体检评分与分阶段行动清单
- 自动生成用户视角描述与智能追问问题（防止需求遗漏）
- 自动生成创新点总结
- 通过 OpenAI / Qwen 生成增强方案文本与协作建议（需配置 API Key）
- GitHub 同步先做“连接信息确认”（Owner/Repo/可见性/默认分支），再生成可推送到指定仓库的脚本

> 当前版本以大模型生成为主，仅支持 OpenAI 兼容 API（OpenAI 或 Qwen）。

## 可选开启大模型增强

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 配置环境变量（示例）：

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="gpt-4.1-mini"  # 可选，不设置则使用默认值
```

或使用 Qwen（DashScope OpenAI 兼容模式）：

```bash
export QWEN_API_KEY="your_qwen_api_key"
# 或者使用 DashScope 常见变量名（等价）：
# export DASHSCOPE_API_KEY="your_qwen_api_key"
export QWEN_MODEL="qwen-plus"  # 可选
export QWEN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 可选
# 也可使用 DASHSCOPE_BASE_URL（等价）：
# export DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

3. 在页面选择提供方（自动/OpenAI/Qwen）并生成方案。  
   - 可直接在界面填写模型名、API Key、Base URL（优先级高于环境变量）。
   - 自动模式：优先使用 `OPENAI_API_KEY`，若不存在则尝试 `QWEN_API_KEY`。
   - 若 OpenAI 返回鉴权/权限类错误（如 `AccessDenied.Unpurchased`、`invalid_api_key`）且已配置 Qwen Key，会自动回退到 Qwen 再尝试一次。
   - 若 Qwen 调用失败，页面会显示错误码、错误信息、模型名与 Base URL，便于快速排查配置问题。
4. 若勾选 GitHub 同步，建议先填写 `GitHub Owner` 与 `GitHub Repo`。系统会先校验连接信息，再输出可直接推送到指定仓库的脚本，并额外生成 `.github/workflows/ci.yml`、Issue/PR 模板建议，支持仓库协作开发。

## 项目结构

```text
ResearchToolAgent/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── __init__.py
│   ├── schemas.py
│   ├── parser.py
│   ├── planner.py
│   ├── ai_planner.py
│   ├── diagram.py
│   ├── explain.py
│   ├── github_publish.py
│   ├── advisor.py
│   ├── humanize.py
│   └── innovation.py
└── docs/
    └── architecture.md
```

## 本地运行

1. 创建并激活虚拟环境（可选）
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 启动应用：

```bash
streamlit run app.py
```

4. 打开浏览器访问提示地址（默认 http://localhost:8501）

## 示例需求

- 开发一个 ONT 信号 chunk 标准化工具
- 开发一个 isoform usage 建模工具
- 开发一个序列错误分析与可视化工具
- 开发一个训练脚本，输入多个 npy 文件，输出分类模型
- 开发一个生信分析流程工具，并自动生成 README 和逻辑图

## Roadmap

- 增强任务分类器（更细颗粒度的科研子任务）
- 加入可配置模板中心与用户自定义规则
- 增加导出能力（Markdown/PDF/zip 骨架）
- 接入测试报告自动生成
- 未来可选接入大模型实现更强的语义理解
