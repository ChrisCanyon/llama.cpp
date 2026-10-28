"""Check that fork changes do not add local artifacts or duplicate source trees."""

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PARTS = {"backup", "snapshot", "source-copy", "old-source", "scratch"}
GENERATED_SUFFIXES = {".exe", ".dll", ".obj", ".pdb", ".gguf", ".safetensors", ".pt"}
LOCAL_PATH = re.compile(r"(?i)(?:[A-Z]:[/\\](?:Users|workspace)[/\\]|file:///)" )
TEXT_SUFFIXES = {".c", ".cc", ".cpp", ".h", ".hpp", ".py", ".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".sh", ".ps1"}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="branch/ref to compare against")
    args = parser.parse_args()
    base = git("merge-base", args.base, "HEAD").decode().strip()
    changed = [p.decode("utf-8") for p in git("diff", "--name-only", "--diff-filter=ACMR", "-z", base, "HEAD").split(b"\0") if p]
    failures = []
    for name in changed:
        path = ROOT / name
        parts = {part.lower() for part in Path(name).parts}
        if parts & FORBIDDEN_PARTS:
            failures.append(f"copied or temporary source tree: {name}")
        if path.suffix.lower() in GENERATED_SUFFIXES:
            failures.append(f"generated binary or model file: {name}")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and path.name != Path(__file__).name:
            if LOCAL_PATH.search(path.read_text(encoding="utf-8", errors="replace")):
                failures.append(f"machine-specific path: {name}")
    if failures:
        print("Fork boundary check failed:\n" + "\n".join(f"- {entry}" for entry in failures), file=sys.stderr)
        return 1
    print(f"Fork boundary check passed: {len(changed)} changed paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
