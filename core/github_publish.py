"""Helpers for direct GitHub publishing guidance."""

from __future__ import annotations

from core.schemas import ResearchSpec


def build_github_publish_steps(spec: ResearchSpec) -> list[str]:
    """Return concrete steps for direct publish to GitHub."""
    repo_name = spec.project_name.lower().replace(" ", "-")
    return [
        "准备 GitHub Personal Access Token（至少包含 repo 权限）。",
        "先执行 Token 可用性校验，确认身份信息返回正常。",
        f"调用 GitHub REST API 创建仓库 `{repo_name}`（可选 private=true）。",
        "本地执行 git init / add / commit 并绑定 origin。",
        "首次 push 到 main 分支后，创建 dev 分支并 push。",
        "开启仓库保护规则与 CI，确保 PR 合并前完成校验。",
    ]


def build_github_token_check_script() -> str:
    """Return script to verify GitHub token and identity before publishing."""
    return "\n".join(
        [
            "# 校验 Token 是否有效（应返回 login/id）",
            "curl -sS https://api.github.com/user -H 'Accept: application/vnd.github+json' -H \"Authorization: Bearer $GITHUB_TOKEN\"",
        ]
    )


def build_github_publish_script(spec: ResearchSpec) -> str:
    """Return copy-ready script for creating repo then pushing code."""
    repo_name = spec.project_name.lower().replace(" ", "-")
    return "\n".join(
        [
            "# 1) 设置环境变量",
            "export GITHUB_TOKEN='<your_pat_with_repo_scope>'",
            "export GITHUB_OWNER='<your_github_username_or_org>'",
            f"export REPO_NAME='{repo_name}'",
            "",
            "# 2) 调用 GitHub API 创建仓库",
            "curl -sS -X POST https://api.github.com/user/repos -H 'Accept: application/vnd.github+json' -H \"Authorization: Bearer $GITHUB_TOKEN\" -d '{\"name\":\"'\"$REPO_NAME\"'\",\"private\":false}'",
            "",
            "# 3) 推送本地代码到 GitHub",
            "git init",
            "git add .",
            "git commit -m 'feat: bootstrap research tool plan'",
            "git branch -M main",
            "git remote add origin https://github.com/$GITHUB_OWNER/$REPO_NAME.git",
            "git push -u origin main",
            "git checkout -b dev",
            "git push -u origin dev",
        ]
    )
