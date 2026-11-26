"""Copy a reviewed, committed standards revision into local repository checkouts."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SHARED = [".github/workflows/link-dependency-issue.yml", "scripts/security_filters.py", "scripts/tests/test_security_filters.py", "scripts/repository_policy.py", "scripts/security_check.py", "scripts/tests/test_repository_policy.py",
          "scripts/tests/test_security_check.py", "requirements-security.txt", "CODE_OF_CONDUCT.md",
          ".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/bug_report.yml",
          ".github/ISSUE_TEMPLATE/feature_request.yml", ".github/ISSUE_TEMPLATE/config.yml", ".github/CODEOWNERS",
          "docs/REPOSITORY-STANDARDS.md"]
HELPERS = ["scripts/build_version.py", "scripts/Publish-WikiGuide.py", "scripts/upload-missing-release-assets.py"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repositories", type=Path, nargs="+")
    args = parser.parse_args()
    managed = SHARED + HELPERS + ["policy/claude-conventions.md"]
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--", *managed], cwd=ROOT, text=True)
    if dirty:
        raise SystemExit("Commit the canonical policy changes before distributing them.")
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    block = (ROOT / "policy/claude-conventions.md").read_text()
    for root in args.repositories:
        if root.resolve() == ROOT.resolve() or not (root / ".github/repository-config.json").is_file():
            raise SystemExit(f"Not a configured consumer repository: {root}")
        files = SHARED + [p for p in HELPERS if (root / p).exists()]
        for name in files:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        claude = root / "CLAUDE.md"
        before, rest = claude.read_text().split("## Repository conventions\n", 1)
        _, after = rest.split("\n## Validation and releases", 1)
        claude.write_text(before + "## Repository conventions\n" + block + "\n## Validation and releases" + after)
        lock = {"version": 1, "source": "DashyNMS/.github", "revision": revision,
                "files": {p: digest(ROOT / p) for p in SHARED},
                "helpers": {p: digest(ROOT / p) for p in HELPERS if (root / p).exists()},
                "claude_sha256": hashlib.sha256(block.encode()).hexdigest()}
        (root / ".github/repository-standards.json").write_text(json.dumps(lock, indent=2) + "\n")
        print(f"{root.name}: copied standards from {revision[:12]}")


if __name__ == "__main__":
    main()
