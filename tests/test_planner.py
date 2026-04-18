import unittest

from core.planner import build_design_plan
from core.schemas import ResearchSpec


class PlannerTests(unittest.TestCase):
    def test_training_plan_is_professional_and_github_aware(self):
        spec = ResearchSpec(
            project_name="NpyClassifier",
            problem_statement="训练分类模型并输出报告",
            task_type="深度学习模型工具",
            input_format="npy",
            output_format="可解释分类模型 + 报告",
            needs_training=True,
            deployment_form="python package + scripts",
            github_sync=True,
            github_owner="demo-user",
            github_repo="demo-repo",
            github_visibility="public",
            github_default_branch="main",
            deliverables=["结构化需求说明"],
        )
        plan = build_design_plan(spec)
        self.assertEqual("阶段 1：数据契约与实验边界", plan[0].title)
        self.assertTrue(any("GitHub Flow" in item for item in plan[-1].items))


if __name__ == "__main__":
    unittest.main()
