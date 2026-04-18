import unittest

from core.planner import build_professional_blueprint
from core.schemas import ResearchSpec


class BlueprintTests(unittest.TestCase):
    def test_blueprint_contains_professional_sections(self):
        spec = ResearchSpec(
            project_name="NpyClassifier",
            problem_statement="训练并输出可解释分类模型",
            task_type="深度学习模型工具",
            input_format="npy",
            output_format="模型 + 报告 + 图表",
            needs_training=True,
            deployment_form="python package + scripts",
            github_sync=False,
            deliverables=["结构化需求说明"],
        )
        blueprint = build_professional_blueprint(spec)
        self.assertIn("vision", blueprint)
        self.assertEqual(4, len(blueprint["architecture_layers"]))
        self.assertTrue(any("科技感" in item for item in blueprint["ux_principles"]))


if __name__ == "__main__":
    unittest.main()
