import unittest

from core.advisor import build_feasibility_report, build_next_actions
from core.humanize import build_clarification_questions
from core.schemas import ResearchSpec


class AdvisorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = ResearchSpec(
            project_name="DemoTool",
            problem_statement="开发一个分类模型工具",
            task_type="深度学习模型工具",
            input_format="npy",
            output_format="分类结果 + 报告",
            needs_training=True,
            deployment_form="python library",
            github_sync=True,
            deliverables=["结构化需求说明"],
        )

    def test_feasibility_report_has_expected_keys(self):
        report = build_feasibility_report(self.spec)
        self.assertIn("overall_score", report)
        self.assertIn("level", report)
        self.assertIn("dimensions", report)
        self.assertGreaterEqual(report["overall_score"], 0)

    def test_next_actions_training_branch(self):
        actions = build_next_actions(self.spec)
        self.assertIn("now", actions)
        self.assertIn("this_week", actions)
        self.assertTrue(any("train/val/test" in item for item in actions["this_week"]))

    def test_clarification_questions_when_complete(self):
        questions = build_clarification_questions(self.spec)
        self.assertGreaterEqual(len(questions), 1)


if __name__ == "__main__":
    unittest.main()
