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
- 自动生成 Mermaid 逻辑流程图
- 自动生成创新点总结

> 当前版本不依赖外部模型 API，不使用数据库，适合离线/内网快速验证。

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
│   ├── diagram.py
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
