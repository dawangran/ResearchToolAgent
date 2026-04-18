"""Explainability helpers for algorithm logic and API responsibilities."""

from __future__ import annotations

from core.schemas import ResearchSpec


def build_algorithm_logic(spec: ResearchSpec) -> list[dict[str, str]]:
    """Return concrete algorithm pipeline steps for the current request."""
    training_mode = "训练闭环" if spec.needs_training else "规则/算法闭环"
    explain_step = "模型可解释性分析（SHAP/特征重要性）" if spec.needs_training else "关键规则可解释性说明"
    return [
        {
            "step": "Step 1 · 数据读取与校验",
            "logic": f"读取 {spec.input_format} 数据，统一样本维度与标签映射，并完成缺失值/异常值检查。",
            "input": f"{spec.input_format} 文件集合 + 元数据（可选）",
            "output": "可训练数据集（X, y）+ 数据质控日志",
        },
        {
            "step": "Step 2 · 特征工程与数据拆分",
            "logic": "执行标准化/特征提取，并按 train/val/test 进行可复现实验拆分。",
            "input": "清洗后的数据集",
            "output": "训练集、验证集、测试集 + 预处理器",
        },
        {
            "step": "Step 3 · 模型训练与调参",
            "logic": f"围绕{training_mode}训练分类器，记录参数、随机种子和关键中间指标。",
            "input": "train/val 数据 + 配置参数",
            "output": "可解释分类模型 + 训练日志 + 最佳参数",
        },
        {
            "step": "Step 4 · 模型评估与可解释性",
            "logic": f"在测试集输出分类指标（Accuracy/F1/AUC）并执行{explain_step}，定位关键特征与误差来源。",
            "input": "已训练模型 + 测试集",
            "output": "评估报告（指标/混淆矩阵）+ 可解释性结果",
        },
        {
            "step": "Step 5 · 产物导出与交付",
            "logic": f"按 {spec.output_format} 组织结果，自动导出图表、报告与可复现运行命令。",
            "input": "模型、评估、解释结果",
            "output": "报告文件 + 可视化图表 + 交付清单",
        },
    ]


def build_api_map(spec: ResearchSpec) -> list[dict[str, str]]:
    """Describe user-project APIs/modules, not ResearchToolAgent internals."""
    return [
        {"api": "load_dataset", "layer": "数据层", "purpose": f"批量读取 {spec.input_format} 并完成样本完整性校验。"},
        {"api": "preprocess_features", "layer": "特征层", "purpose": "执行标准化、特征构建与数据集切分，保证训练可复现。"},
        {"api": "train_classifier", "layer": "训练层", "purpose": "训练分类模型并保存最佳权重、参数与训练日志。"},
        {"api": "evaluate_model", "layer": "评估层", "purpose": "计算 Accuracy/F1/AUC、输出混淆矩阵和误差样本分析。"},
        {"api": "explain_predictions", "layer": "解释层", "purpose": "生成 SHAP/特征重要性结果，解释模型决策依据。"},
        {"api": "build_report", "layer": "报告层", "purpose": f"汇总指标、图表与结论，输出 {spec.output_format}。"},
        {"api": "export_artifacts", "layer": "交付层", "purpose": "统一导出模型文件、图表、日志与可复现命令。"},
    ]


def build_algorithm_sequence_mermaid(spec: ResearchSpec) -> str:
    """Generate a cleaner sequence diagram for logic walkthrough."""
    return f"""sequenceDiagram
    autonumber
    participant U as 用户
    participant DS as Dataset Loader
    participant PP as Preprocessor
    participant TR as Trainer
    participant EV as Evaluator
    participant EX as Explainer
    participant RP as Reporter

    U->>DS: 提供 {spec.input_format} 数据与配置
    DS-->>PP: 清洗后数据 + 质控日志
    PP-->>TR: 训练/验证/测试集
    TR-->>EV: 已训练分类模型
    EV-->>EX: 评估结果 + 预测输出
    EX-->>RP: 特征贡献与可解释结论
    RP-->>U: {spec.output_format}
"""
