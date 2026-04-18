"""Helpers for direct GitHub publishing guidance."""

from __future__ import annotations

import re

from core.schemas import ResearchSpec


_OWNER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
_REPO_RE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
_BRANCH_RE = re.compile(r"^(?!/)(?!.*//)[^\s~^:?*\[\]]+$")


def build_github_preflight(spec: ResearchSpec) -> dict[str, object]:
    """Validate GitHub sync fields before giving publish instructions."""
    errors: list[str] = []
    warnings: list[str] = []

    if not spec.github_sync:
        return {"ready": True, "errors": [], "warnings": ["未开启 GitHub 同步，已跳过同步预检。"]}

    owner = spec.github_owner.strip()
    repo = spec.github_repo.strip()
    branch = spec.github_default_branch.strip()

    if not owner:
        errors.append("缺少 GitHub Owner（用户名或组织名）。")
    elif not _OWNER_RE.match(owner):
        errors.append("GitHub Owner 格式不合法：仅允许字母、数字、短横线，且不能以短横线开头或结尾。")

    if not repo:
        errors.append("缺少 GitHub Repo（仓库名）。")
    elif not _REPO_RE.match(repo):
        errors.append("GitHub Repo 格式不合法：建议使用字母、数字、点、下划线、短横线。")

    if not branch:
        errors.append("缺少默认分支名（例如 main）。")
    elif not _BRANCH_RE.match(branch):
        errors.append("默认分支名格式不合法：不能包含空格及 Git 禁止字符。")

    if spec.github_visibility not in {"public", "private"}:
        warnings.append("仓库可见性异常，已回退为 public。")

    if owner and repo:
        warnings.append(f"目标仓库：{owner}/{repo}")

    return {"ready": len(errors) == 0, "errors": errors, "warnings": warnings}


def build_github_publish_steps(spec: ResearchSpec) -> list[str]:
    """Return concrete steps for direct publish to GitHub."""
    repo_name = spec.github_repo or spec.project_name.lower().replace(" ", "-")
    owner_text = spec.github_owner or "<your_github_username_or_org>"
    visibility_text = "private=true" if spec.github_visibility == "private" else "private=false"
    return [
        "【先做人性化确认】明确同步目标：是否开启 GitHub 同步、仓库归属、仓库名、可见性、默认分支。",
        "准备 GitHub Personal Access Token（至少包含 repo 权限），建议用最小权限 + 到期时间。",
        "先执行 Token 可用性校验，确认身份信息返回正常，再继续后续步骤。",
        f"调用 GitHub REST API 在 `{owner_text}` 下创建仓库 `{repo_name}`（{visibility_text}）。",
        f"本地执行 git init / add / commit 并绑定 origin，首次 push 到 `{spec.github_default_branch}`。",
        "若需要协作分支，再创建 dev 或 feature/* 分支，并启用保护规则与 CI。",
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
    repo_name = spec.github_repo or spec.project_name.lower().replace(" ", "-")
    owner_name = spec.github_owner or "<your_github_username_or_org>"
    branch_name = spec.github_default_branch or "main"
    private_flag = "true" if spec.github_visibility == "private" else "false"
    return "\n".join(
        [
            "# 0) 先设置 Git 身份（首次机器必做）",
            "git config --global user.name '<your_name>'",
            "git config --global user.email '<your_email>'",
            "",
            "# 1) 设置 GitHub 连接信息（建议先填这里，再执行后续步骤）",
            "export GITHUB_TOKEN='<your_pat_with_repo_scope>'",
            f"export GITHUB_OWNER='{owner_name}'",
            f"export REPO_NAME='{repo_name}'",
            f"export DEFAULT_BRANCH='{branch_name}'",
            f"export REPO_PRIVATE='{private_flag}'",
            "",
            "# 2) 校验 Token 可用性（若无 login 字段，请先排查）",
            "curl -sS https://api.github.com/user -H 'Accept: application/vnd.github+json' -H \"Authorization: Bearer $GITHUB_TOKEN\"",
            "",
            "# 3) 调用 GitHub API 创建仓库（个人账号可用 /user/repos；组织可改为 /orgs/$GITHUB_OWNER/repos）",
            "curl -sS -X POST https://api.github.com/user/repos -H 'Accept: application/vnd.github+json' -H \"Authorization: Bearer $GITHUB_TOKEN\" -d '{\"name\":\"'\"$REPO_NAME\"'\",\"private\":'\"$REPO_PRIVATE\"'}'",
            "",
            "# 4) 推送本地代码到 GitHub",
            "git init",
            "git add .",
            "git commit -m 'feat: bootstrap research tool plan'",
            "git branch -M \"$DEFAULT_BRANCH\"",
            "git remote add origin https://github.com/$GITHUB_OWNER/$REPO_NAME.git",
            "git push -u origin \"$DEFAULT_BRANCH\"",
            "",
            "# 5) 可选：创建协作分支",
            "git checkout -b dev",
            "git push -u origin dev",
        ]
    )
