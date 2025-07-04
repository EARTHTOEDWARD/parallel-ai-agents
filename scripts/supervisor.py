#!/usr/bin/env python3
"""
Supervisor/Collator Script for Parallel AI Agents
Manages outputs from multiple Claude agents and coordinates merges
"""

import json
import subprocess
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Tuple
import argparse
import os


class AgentSupervisor:
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.agents = {
            "backend-opus": {
                "branch": "backend-opus",
                "paths": ["backend/", "docs/api/"],
                "test_command": "cd backend && npm test",
            },
            "frontend-opus": {
                "branch": "frontend-opus",
                "paths": ["frontend/", "docs/ui/"],
                "test_command": "cd frontend && npm test",
            },
            "test-opus": {
                "branch": "test-opus",
                "paths": ["tests/", "docs/testing/"],
                "test_command": "npm test",
            },
        }
        self.reports_dir = self.project_root / "supervisor-reports"
        self.reports_dir.mkdir(exist_ok=True)

    def run_command(self, cmd: str, cwd: Path = None) -> Tuple[int, str, str]:
        """Execute shell command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def get_branch_status(self, branch: str) -> Dict:
        """Get status of a specific agent branch"""
        # Switch to branch
        self.run_command(f"git checkout {branch}")

        # Get diff from main
        _, diff_output, _ = self.run_command("git diff main --stat")

        # Get recent commits
        _, log_output, _ = self.run_command("git log main..HEAD --oneline")

        # Run tests if configured
        agent_config = self.agents.get(branch, {})
        test_results = None
        if test_cmd := agent_config.get("test_command"):
            exit_code, stdout, stderr = self.run_command(test_cmd)
            test_results = {
                "passed": exit_code == 0,
                "output": stdout if exit_code == 0 else stderr,
            }

        # Check linting
        lint_code, lint_out, _ = self.run_command("npm run lint")

        # Get coverage if available
        _, coverage_out, _ = self.run_command(
            "npm run test:coverage -- --json --outputFile=coverage.json"
        )
        coverage = None
        coverage_file = self.project_root / "coverage.json"
        if coverage_file.exists():
            with open(coverage_file) as f:
                coverage_data = json.load(f)
                coverage = coverage_data.get("total", {}).get("lines", {}).get("pct", 0)

        return {
            "branch": branch,
            "commits": log_output.strip().split("\n") if log_output.strip() else [],
            "files_changed": (
                len(diff_output.strip().split("\n")) if diff_output.strip() else 0
            ),
            "tests": test_results,
            "linting": {
                "passed": lint_code == 0,
                "issues": lint_out if lint_code != 0 else None,
            },
            "coverage": coverage,
            "diff_stat": diff_output,
        }

    def load_llm_usage(self) -> Dict:
        """Load LLM usage data from temporary file"""
        try:
            with open("/tmp/llm_usage.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"tokens": 0}

    def generate_summary(self, statuses: Dict[str, Dict]) -> str:
        """Generate human-readable summary of all agent statuses"""
        summary_lines = [
            "# Parallel AI Agent Status Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        for agent, status in statuses.items():
            summary_lines.extend(
                [
                    f"## {agent}",
                    f"- Commits: {len(status['commits'])}",
                    f"- Files changed: {status['files_changed']}",
                ]
            )

            if status["tests"]:
                test_status = "✅ PASSED" if status["tests"]["passed"] else "❌ FAILED"
                summary_lines.append(f"- Tests: {test_status}")

            lint_status = "✅ PASSED" if status["linting"]["passed"] else "❌ FAILED"
            summary_lines.append(f"- Linting: {lint_status}")

            if status["coverage"]:
                summary_lines.append(f"- Coverage: {status['coverage']}%")

            summary_lines.append("")

        # Add merge recommendations
        summary_lines.extend(["## Merge Recommendations", ""])

        ready_to_merge = []
        needs_work = []

        for agent, status in statuses.items():
            if status.get("tests", {}).get("passed", False) and status.get(
                "linting", {}
            ).get("passed", False):
                ready_to_merge.append(agent)
            else:
                needs_work.append(agent)

        if ready_to_merge:
            summary_lines.append("### Ready to merge:")
            for agent in ready_to_merge:
                summary_lines.append(f"- {agent}")
            summary_lines.append("")

        if needs_work:
            summary_lines.append("### Needs attention:")
            for agent in needs_work:
                status = statuses[agent]
                issues = []
                if not status.get("tests", {}).get("passed", False):
                    issues.append("failing tests")
                if not status.get("linting", {}).get("passed", False):
                    issues.append("linting errors")
                summary_lines.append(f"- {agent}: {', '.join(issues)}")

        # Add LLM usage information
        summary_lines.extend(["## LLM Usage", ""])
        usage_data = self.load_llm_usage()
        if usage_data:
            budget = os.getenv("DAILY_TOKEN_BUDGET", "200000")
            summary_lines.append(
                f"[SUPERVISOR] {date.today()} :: "
                f"LLM tokens used today: {usage_data.get('tokens', 0)} / {budget}"
            )
        else:
            summary_lines.append("No LLM usage data available")

        return "\n".join(summary_lines)

    def check_merge_conflicts(self, branch: str) -> Tuple[bool, str]:
        """Check if branch can be merged cleanly into main"""
        self.run_command("git checkout main")
        exit_code, stdout, stderr = self.run_command(
            f"git merge --no-commit --no-ff {branch}"
        )
        self.run_command("git merge --abort")  # Clean up

        has_conflicts = exit_code != 0
        return not has_conflicts, stderr if has_conflicts else ""

    def create_pull_request(self, branch: str, title: str, body: str):
        """Create a pull request using GitHub CLI if available"""
        # Check if gh is installed
        gh_check, _, _ = self.run_command("which gh")
        if gh_check != 0:
            print("GitHub CLI not installed. Install with: brew install gh")
            return

        cmd = f'gh pr create --base main --head {branch} --title "{title}" --body "{body}"'
        exit_code, stdout, stderr = self.run_command(cmd)

        if exit_code == 0:
            print(f"Pull request created: {stdout}")
        else:
            print(f"Failed to create PR: {stderr}")

    def monitor_agents(self, create_prs: bool = False):
        """Main monitoring loop"""
        print("🤖 Supervisor starting agent monitoring...")

        # Save current branch to restore later
        _, current_branch, _ = self.run_command("git branch --show-current")
        current_branch = current_branch.strip()

        statuses = {}

        for agent_name in self.agents.keys():
            print(f"\n📊 Checking {agent_name}...")
            statuses[agent_name] = self.get_branch_status(agent_name)

        # Generate summary
        summary = self.generate_summary(statuses)

        # Save report
        report_file = (
            self.reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        with open(report_file, "w") as f:
            f.write(summary)

        print(f"\n📄 Report saved to: {report_file}")
        print("\n" + "=" * 50)
        print(summary)
        print("=" * 50 + "\n")

        # Create PRs if requested
        if create_prs:
            for agent_name, status in statuses.items():
                if (
                    status.get("tests", {}).get("passed", False)
                    and status.get("linting", {}).get("passed", False)
                    and len(status["commits"]) > 0
                ):

                    can_merge, conflicts = self.check_merge_conflicts(agent_name)
                    if can_merge:
                        title = f"[{agent_name}] Updates from AI agent"
                        body = f"Automated PR from {agent_name}\n\n"
                        body += f"Commits: {len(status['commits'])}\n"
                        body += f"Files changed: {status['files_changed']}\n"
                        body += "Tests: ✅ Passing\n"
                        body += "Linting: ✅ Clean\n"
                        if status["coverage"]:
                            body += f"Coverage: {status['coverage']}%\n"

                        self.create_pull_request(agent_name, title, body)

        # Restore original branch
        self.run_command(f"git checkout {current_branch}")

    def merge_branch(self, branch: str, squash: bool = False):
        """Merge an agent branch into main"""
        print(f"\n🔀 Merging {branch} into main...")

        self.run_command("git checkout main")

        merge_cmd = "git merge"
        if squash:
            merge_cmd += " --squash"
        merge_cmd += f" {branch}"

        exit_code, stdout, stderr = self.run_command(merge_cmd)

        if exit_code == 0:
            if squash:
                # Need to commit after squash merge
                self.run_command(f'git commit -m "Merge {branch} (squashed)"')
            print(f"✅ Successfully merged {branch}")
        else:
            print(f"❌ Merge failed: {stderr}")
            print("Run 'git status' to see conflicts")


def main():
    parser = argparse.ArgumentParser(description="Supervisor for Parallel AI Agents")
    parser.add_argument(
        "--monitor", action="store_true", help="Monitor all agents and generate report"
    )
    parser.add_argument(
        "--merge", type=str, help="Merge specified agent branch into main"
    )
    parser.add_argument(
        "--squash", action="store_true", help="Squash commits when merging"
    )
    parser.add_argument(
        "--create-prs", action="store_true", help="Create PRs for ready branches"
    )
    parser.add_argument(
        "--project-root", type=Path, default=Path.cwd(), help="Project root directory"
    )

    args = parser.parse_args()

    supervisor = AgentSupervisor(project_root=args.project_root)

    if args.monitor:
        supervisor.monitor_agents(create_prs=args.create_prs)
    elif args.merge:
        supervisor.merge_branch(args.merge, squash=args.squash)
    else:
        # Default: monitor without creating PRs
        supervisor.monitor_agents(create_prs=False)


if __name__ == "__main__":
    main()
