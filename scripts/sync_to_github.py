#!/usr/bin/env python3
"""
sync_to_github.py — 将本地构建产物同步到 GitHub 仓库并自动 commit + push。

依赖：
    - Git（命令行可用）
    - 已配置 SSH 公钥（git@github.com 可达）

用法：
    python sync_to_github.py

环境变量（可选）：
    CRC_KB_REPO   - GitHub 仓库根目录（默认从脚本位置向上查找）
    CRC_KB_REMOTE - remote 名称（默认 origin）
    CRC_KB_BRANCH - 分支名（默认 main）
    SKIP_BUILD    - 设为 1 则跳过 build_kb.py 直接同步
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime

# ============================================================
# 路径配置
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.environ.get("CRC_KB_REPO", os.path.dirname(SCRIPT_DIR))
REMOTE     = os.environ.get("CRC_KB_REMOTE", "origin")
BRANCH     = os.environ.get("CRC_KB_BRANCH", "main")

# 需要同步的关键文件（相对路径，相对于 REPO_ROOT）
SYNC_FILES = [
    "data/kb.json",
    "data/kb_meta.json",
    "data/knowledge-graph/",
    "CHANGELOG.md",
    "UPDATE_POLICY.md",
    "README.md",
]

# ============================================================
# 工具函数
# ============================================================

def run(cmd: str, cwd: str = REPO_ROOT, check: bool = True) -> subprocess.CompletedProcess:
    """运行 shell 命令，失败时退出"""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        print(f"❌ 命令失败: {cmd}")
        print(f"   stdout: {result.stdout}")
        print(f"   stderr: {result.stderr}")
        sys.exit(1)
    return result


def git_current_commit_message() -> str:
    """获取当前的 HEAD commit message（用于判断是否有未 push 的内容）"""
    result = run(f'git log -1 --format="%s" {REMOTE}/{BRANCH}..HEAD 2>/dev/null || true')
    return result.stdout.strip()


def file_changed(path: str) -> bool:
    """检查文件相对于 origin/{branch} 是否有变更"""
    result = run(
        f'git diff --name-only {REMOTE}/{BRANCH} HEAD -- "{path}" 2>/dev/null | grep -q .',
        check=False,
    )
    return result.returncode == 0


def kb_summary() -> str:
    """读取 kb_meta.json，提取条目数/版本/日期"""
    meta_path = os.path.join(REPO_ROOT, "data/kb_meta.json")
    if not os.path.exists(meta_path):
        return "unknown"
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    version = meta.get("version", "?")
    date    = meta.get("update_date", "?")
    total   = meta.get("total_entries", "?")
    return f"v{version} | {total} 条 | {date}"


def new_batch_files() -> list[str]:
    """找出知识图谱目录下本次新增的批次文件"""
    kg_dir = os.path.join(REPO_ROOT, "data/knowledge-graph")
    files = []
    if os.path.isdir(kg_dir):
        for fname in sorted(os.listdir(kg_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(kg_dir, fname)
                # 检查文件修改时间 >24h（避免误判当前正在写入的文件）
                mtime = os.path.getmtime(fpath)
                age_h = (datetime.now().timestamp() - mtime) / 3600
                if age_h > 0.5:
                    files.append(fname)
    return files


def generate_commit_message() -> str:
    """生成有意义的 commit message"""
    meta_path = os.path.join(REPO_ROOT, "data/kb_meta.json")
    date = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        total = meta.get("total_entries", "?")
        new_files = new_batch_files()
        if new_files:
            file_note = " | ".join(new_files[:3])
            if len(new_files) > 3:
                file_note += f" (+{len(new_files)-3} 个文件)"
        else:
            file_note = "批次更新"

        return (
            f"feat: 知识库更新至 {total} 条 ({date})\n\n"
            f"- 新增文件: {file_note}\n"
            f"- 版本: v{meta.get('version', '?')}"
        )
    else:
        return f"chore: 同步更新 ({date})"


# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 50)
    print(f"🚀 GitHub 同步 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 1. 检查 Git 状态
    print("\n📂 检查仓库状态...")
    status = run("git status --porcelain", check=False)
    dirty_files = [l for l in status.stdout.strip().split("\n") if l]

    if not dirty_files:
        print("✅ 没有变更需要同步")
        print(f"   当前知识库: {kb_summary()}")
        return

    print(f"   待同步文件: {len(dirty_files)} 个")
    for f in dirty_files[:10]:
        print(f"     {f}")
    if len(dirty_files) > 10:
        print(f"     ... 还有 {len(dirty_files)-10} 个")

    # 2. 可选：运行 build（默认执行）
    skip_build = os.environ.get("SKIP_BUILD", "0") == "1"
    if not skip_build:
        print("\n🔨 运行知识库构建...")
        build_script = os.path.join(SCRIPT_DIR, "build_kb.py")
        if os.path.exists(build_script):
            result = run(f"python3 '{build_script}'", check=False)
            print(result.stdout)
            if result.returncode != 0:
                print(f"⚠️  build 脚本执行失败（继续同步）: {result.stderr}")
        else:
            print(f"⚠️  build_kb.py 未找到，跳过构建阶段")

    # 3. Stage 所有变更
    print("\n📦 Stage 变更文件...")
    run("git add -A")

    # 4. 生成 commit message
    msg = generate_commit_message()
    print(f"\n📝 Commit message:\n{msg}")

    # 5. Commit
    print("\n💾 Committing...")
    # 使用 HEREDOC 避免 shell 注入
    run(f'git commit -F - <<"EOF"\n{msg}\nEOF')

    # 6. Push
    print(f"\n📤 Pushing to {REMOTE}/{BRANCH}...")
    push_result = run(f"git push {REMOTE} {BRANCH}", check=False)

    if push_result.returncode == 0:
        print(f"✅ 同步完成!")
        print(f"   知识库: {kb_summary()}")
    else:
        print(f"❌ Push 失败: {push_result.stderr}")
        print(f"   本地 commit 已创建，可稍后手动: git push {REMOTE} {BRANCH}")

    # 7. 显示最新 commit
    print("\n📋 最新 Commit:")
    print(run("git log -1 --stat").stdout)


if __name__ == "__main__":
    main()
