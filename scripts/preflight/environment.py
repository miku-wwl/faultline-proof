"""Read-only local tool inventory. Never reads credentials or contacts a cloud API."""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def version(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        # Version commands only; do not collect environment or full Docker inspect.
        return {
            "exit_code": result.returncode,
            "version": (result.stdout + result.stderr).strip()[:300],
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"status": "UNAVAILABLE", "error_type": type(error).__name__}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    commands = {
        "uv": ["uv", "--version"],
        "git": ["git", "--version"],
        "docker": [
            "docker",
            "version",
            "--format",
            "{{.Client.Version}}/{{.Server.Version}}",
        ],
        "compose": ["docker", "compose", "version"],
        "node": ["node", "--version"],
        "npm": ["npm.cmd" if os.name == "nt" else "npm", "--version"],
        "powershell": [
            "pwsh",
            "-NoProfile",
            "-Command",
            "$PSVersionTable.PSVersion.ToString()",
        ],
        "openssh": ["ssh", "-V"],
        "terraform": ["terraform", "version", "-json"],
    }
    result = {
        "schema": "generic-environment-preflight-v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "project_venv": sys.prefix != sys.base_prefix,
        "tools": {
            name: version(cmd) if shutil.which(cmd[0]) else {"status": "MISSING"}
            for name, cmd in commands.items()
        },
        "credential_presence_process_only": {
            name: "PRESENT" if os.environ.get(name, "").strip() else "MISSING"
            for name in (
                "VULTR_API_KEY",
                "VULTR_API_TOKEN",
                "VULTR_INFERENCE_API_KEY",
                "VULTR_INFERENCE_KEY",
            )
        },
        "cloud_account": "UNVERIFIED",
        "cloud_calls": "NOT RUN",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if sys.version_info[:2] == (3, 13) and sys.prefix != sys.base_prefix else 1


if __name__ == "__main__":
    raise SystemExit(main())
