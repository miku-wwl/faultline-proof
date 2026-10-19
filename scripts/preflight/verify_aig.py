"""Qualify an installed pinned dependency, without creating any Run or Action."""

import argparse
import base64
import csv
import hashlib
import importlib.metadata
import inspect
import json
import platform
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

from agentic_intent_gate import runtime

PIN = "7261fdd2f47d2b15fabe8faac527eeee37338eb1"
URL = "https://github.com/miku-wwl/agentic-intent-gate"
EXPORTS = (
    "ToolBinding",
    "ToolCapability",
    "ExecutableRegistry",
    "CapabilityVerifier",
    "BoundCapabilityAuthorization",
    "open_runtime",
    "execution_budget_binding",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    project = tomllib.loads((root / "pyproject.toml").read_text("utf-8"))
    lock = tomllib.loads((root / "uv.lock").read_text("utf-8"))
    dist = importlib.metadata.distribution("agentic-intent-gate")
    direct = json.loads(dist.read_text("direct_url.json"))
    source = Path(runtime.__file__).resolve()
    expected_source = Path(sys.prefix).resolve() / (
        "Lib/site-packages"
        if sys.platform == "win32"
        else "lib/python3.13/site-packages"
    )
    locked = [p for p in lock["package"] if p["name"] == "agentic-intent-gate"]
    checks = {
        "python_3_13": sys.version_info[:2] == (3, 13),
        "project_local_venv": Path(sys.prefix).resolve() == root / ".venv",
        "version_0_2_0": dist.version == "0.2.0",
        "direct_git_commit": direct.get("vcs_info", {}).get("commit_id") == PIN,
        "direct_https_url": direct.get("url", "").removesuffix(".git") == URL,
        "installed_site_packages_import": source.is_relative_to(expected_source),
        "manifest_exact_pin": f"agentic-intent-gate @ git+{URL}.git@{PIN}"
        in project["project"]["dependencies"],
        "lock_exact_pin": len(locked) == 1
        and locked[0]["version"] == "0.2.0"
        and locked[0]["source"].get("git") == f"{URL}.git?rev={PIN}#{PIN}",
        "public_exports": all(hasattr(runtime, name) for name in EXPORTS),
        "default_five_seconds": inspect.signature(runtime.open_runtime)
        .parameters["execution_timeout_seconds"]
        .default
        == 5,
    }
    hashed_count, mismatches = 0, []
    for relpath, recorded, _size in csv.reader(dist.read_text("RECORD").splitlines()):
        if not recorded:
            continue
        algo, encoded = recorded.split("=", 1)
        actual = hashlib.new(
            algo, Path(dist.locate_file(relpath)).read_bytes()
        ).digest()
        hashed_count += 1
        if base64.urlsafe_b64encode(actual).decode().rstrip("=") != encoded:
            mismatches.append(relpath)
    checks["installed_record_hashes"] = hashed_count > 0 and not mismatches
    result = {
        "schema": "aig-installed-dependency-preflight-v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "python": platform.python_version(),
        "distribution_version": dist.version,
        "direct_url": direct,
        "import_location_relative_to_project": source.relative_to(root).as_posix(),
        "checks": checks,
        "record_hash_count": hashed_count,
        "record_mismatches": mismatches,
        "public_signatures": {
            name: str(inspect.signature(getattr(runtime, name))) for name in EXPORTS
        },
        "lock_sha256": hashlib.sha256((root / "uv.lock").read_bytes()).hexdigest(),
        "product_adapter": "NOT IMPLEMENTED",
        "runtime_action_execution": "NOT RUN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
