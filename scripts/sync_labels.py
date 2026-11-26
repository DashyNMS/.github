"""Synchronise shared labels while preserving repository-specific classifications."""
import argparse
import json
from pathlib import Path
import subprocess
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def request(token, path, method="GET", data=None):
    payload = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request("https://api.github.com/" + path, data=payload, method=method,
                                 headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    # Requests are constructed exclusively against the fixed GitHub HTTPS API.
    with urllib.request.urlopen(req, timeout=30) as response:  # nosec B310
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repositories", nargs="+", choices=["core", "desktop", "mobile", "mcp", "sensor-definitions", ".github", "website"])
    parser.add_argument("--apply", action="store_true", help="apply the displayed changes; default is a dry run")
    args = parser.parse_args()
    token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    manifest = json.loads((ROOT / "policy/labels.json").read_text())
    for repo in args.repositories:
        path = f"repos/DashyNMS/{repo}/labels"
        existing = []
        for page in range(1, 21):
            batch = request(token, f"{path}?per_page=100&page={page}")
            existing += batch
            if len(batch) < 100:
                break
        else:
            raise SystemExit("Label pagination exceeded its limit; no partial sync was applied.")
        indexed = {label["name"].casefold(): label for label in existing}
        wanted = manifest["labels"] + [dict(name=name, **entry) for name, entry in manifest["ecosystems"].items()
                                       if name.casefold() in indexed or name in ({"github_actions"} | ({"python"} if repo in ("sensor-definitions", ".github", "mobile", "website") else set()) | ({".NET"} if repo in ("core", "desktop", "mobile", "mcp") else set()) | ({"docker"} if repo == "mcp" else set()))]
        for label in wanted:
            old = indexed.get(label["name"].casefold())
            if old and all(old.get(key) == value for key, value in label.items()):
                continue
            print(f"{repo}: {'update' if old else 'create'} {label['name']}")
            if args.apply:
                if old:
                    request(token, path + "/" + urllib.parse.quote(old["name"], safe=""), "PATCH",
                            dict(new_name=label["name"], color=label["color"], description=label["description"]))
                else:
                    request(token, path, "POST", label)


if __name__ == "__main__":
    main()
