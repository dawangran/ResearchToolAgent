import unittest

from core.github_publish import build_github_publish_script, build_github_publish_steps
from core.schemas import ResearchSpec


class GithubPublishTests(unittest.TestCase):
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
            github_owner="demo-user",
            github_repo="demo-repo",
            github_visibility="private",
            github_default_branch="main",
            deliverables=["结构化需求说明"],
        )

    def test_publish_steps_start_with_connection_confirmation(self):
        steps = build_github_publish_steps(self.spec)
        self.assertIn("明确同步目标", steps[0])
        self.assertIn("demo-user", "".join(steps))
        self.assertIn("demo-repo", "".join(steps))

    def test_publish_script_contains_target_repo_config(self):
        script = build_github_publish_script(self.spec)
        self.assertIn("export GITHUB_OWNER='demo-user'", script)
        self.assertIn("export REPO_NAME='demo-repo'", script)
        self.assertIn("export REPO_PRIVATE='true'", script)
        self.assertIn('git push -u origin "$DEFAULT_BRANCH"', script)


if __name__ == "__main__":
    unittest.main()
