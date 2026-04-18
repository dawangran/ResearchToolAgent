import unittest

from core.diagram import build_diagram_explanation, generate_mermaid_flow
from core.explain import build_algorithm_logic, build_algorithm_sequence_mermaid, build_api_map
from core.innovation import generate_innovation_points
from core.schemas import ResearchSpec


class ProjectOrientedOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = ResearchSpec(
            project_name="NpyClassifier",
            problem_statement="开发一个训练脚本，输入多个 npy 文件，输出一个可解释的分类模型，并自动生成评估报告和可视化图表。",
            task_type="深度学习模型工具",
            input_format="npy",
            output_format="可解释分类模型 + 评估报告 + 可视化图表",
            needs_training=True,
            deployment_form="python package + scripts",
            github_sync=False,
            deliverables=["结构化需求说明"],
        )

    def test_algorithm_logic_focuses_on_user_project_pipeline(self):
        logic = build_algorithm_logic(self.spec)
        all_text = " ".join(item["logic"] for item in logic)
        self.assertIn("数据", all_text)
        self.assertIn("分类指标", all_text)
        self.assertNotIn("自然语言需求", all_text)

    def test_api_map_is_project_oriented(self):
        api_map = build_api_map(self.spec)
        merged = " ".join(item["api"] for item in api_map)
        self.assertIn("train_classifier", merged)
        self.assertNotIn("parse_user_request", merged)

    def test_diagram_and_innovation_are_project_oriented(self):
        mermaid = generate_mermaid_flow(self.spec.task_type)
        seq = build_algorithm_sequence_mermaid(self.spec)
        note = build_diagram_explanation(self.spec.task_type)
        points = " ".join(generate_innovation_points(self.spec))
        self.assertIn("模型训练与调参", mermaid)
        self.assertIn("Dataset Loader", seq)
        self.assertIn("业务工具本身", note)
        self.assertIn("pipeline", points)


if __name__ == "__main__":
    unittest.main()
