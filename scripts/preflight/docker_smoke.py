"""Opt-in generic Docker capability check; no incident, worker, agent or cloud code."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

PROBE = r"""set -eu
test "$(id -u)" = 65534
echo uid=$(id -u)
awk '$2 == "/" {n=split($4,a,","); for(i=1;i<=n;i++) if(a[i]=="ro") print "root_readonly=true"}' /proc/mounts
test "$(cat /input/marker)" = generic-read-only-marker
if (echo changed > /input/marker) 2>/dev/null; then exit 41; fi
echo bind_write=denied
echo scratch > /tmp/scratch
test -f /tmp/scratch
echo tmpfs_write=allowed
test ! -S /var/run/docker.sock
echo docker_socket=absent
awk '/^CapEff:/ {print "cap_eff=" $2} /^NoNewPrivs:/ {print "no_new_privs=" $2} /^Seccomp:/ {print "seccomp=" $2}' /proc/self/status
echo memory_max=$(cat /sys/fs/cgroup/memory.max)
echo swap_max=$(cat /sys/fs/cgroup/memory.swap.max)
echo pids_max=$(cat /sys/fs/cgroup/pids.max)
echo cpu_max=$(cat /sys/fs/cgroup/cpu.max)
echo interfaces=$(ls /sys/class/net)
if nc -z -w 1 1.1.1.1 443 2>/dev/null; then exit 42; fi
echo external_tcp=denied
echo ready=true
exec sleep 60
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--context", required=True, help="Explicit local Docker context"
    )
    parser.add_argument(
        "--image", required=True, help="Already pulled official Alpine digest"
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch(
        r"(?:docker.io/library/)?alpine@sha256:[a-f0-9]{64}", args.image
    ):
        parser.error(
            "Use an immutable official Alpine image digest, never a mutable tag"
        )
    # Never inherit a remote daemon override or silently change the ambient context.
    if any(os.environ.get(k) for k in ("DOCKER_HOST", "DOCKER_CONTEXT")):
        parser.error("Unset Docker endpoint overrides before this explicit local check")
    root = Path(__file__).resolve().parents[2]
    local = root / ".local"
    local.mkdir(exist_ok=True)
    if local.is_symlink() or local.resolve().parent != root:
        parser.error(
            "Scratch root must be inside the project and must not be a symlink"
        )
    scope = str(uuid4())
    name = "generic-preflight-" + scope
    label = "io.faultline.preflight=" + scope
    command = ["docker", "--context", args.context]
    result = {
        "schema": "generic-docker-capability-preflight-v1",
        "scope": scope,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "image": args.image,
        "context": args.context,
        "checks": {},
        "status": "FAIL",
        "cloud_containment": "NOT RUN",
        "stress_or_escape_tests": "NOT RUN",
        "events": [],
    }
    checks = result["checks"]

    def docker(*parts, timeout=20, check=True):
        proc = subprocess.run(
            command + list(parts), capture_output=True, text=True, timeout=timeout
        )
        if check and proc.returncode:
            raise RuntimeError(
                "docker " + parts[0] + " failed, exit=" + str(proc.returncode)
            )
        return proc

    before = set()
    directory = Path(tempfile.mkdtemp(prefix="docker-smoke-", dir=local)).resolve()
    marker = directory / "marker"
    marker.write_bytes(b"generic-read-only-marker\n")
    directory.chmod(0o755)
    marker.chmod(0o644)
    marker_hash = hashlib.sha256(marker.read_bytes()).hexdigest()
    try:
        context = json.loads(docker("context", "inspect", args.context).stdout)[0]
        endpoint = context["Endpoints"]["docker"]["Host"]
        if not (endpoint.startswith("npipe://") or endpoint.startswith("unix://")):
            raise RuntimeError(
                "Only a local Unix socket or Windows named pipe is allowed"
            )
        info = json.loads(docker("info", "--format", "{{json .}}").stdout)
        result["daemon"] = {
            key: info.get(key)
            for key in (
                "ServerVersion",
                "OSType",
                "Architecture",
                "KernelVersion",
                "OperatingSystem",
                "CgroupVersion",
                "CgroupDriver",
                "NCPU",
                "MemTotal",
                "SecurityOptions",
            )
        }
        if info["OSType"] != "linux" or str(info["CgroupVersion"]) != "2":
            raise RuntimeError("This smoke check requires Linux and cgroup v2")
        before = set(docker("ps", "-aq", "--no-trunc").stdout.split())
        result["preexisting_container_count"] = len(before)
        image = json.loads(docker("image", "inspect", args.image).stdout)[0]
        result["local_image_id"] = image["Id"]
        result["events"].append("create_requested")
        docker(
            "create",
            "--name",
            name,
            "--label",
            label,
            "--pull=never",
            "--read-only",
            "--user",
            "65534:65534",
            "--network",
            "none",
            "--cpus",
            "0.25",
            "--memory",
            "64m",
            "--memory-swap",
            "64m",
            "--pids-limit",
            "32",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges=true",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,nodev,size=16777216,mode=1777",
            "--ulimit",
            "nofile=128:128",
            "--log-opt",
            "max-size=1m",
            "--log-opt",
            "max-file=1",
            "--mount",
            f"type=bind,src={directory},dst=/input,readonly",
            args.image,
            "sh",
            "-c",
            PROBE,
        )
        observed = json.loads(docker("inspect", name).stdout)[0]
        result["container_id"] = observed["Id"]
        host = observed["HostConfig"]
        checks.update(
            {
                "readonly_root_config": host["ReadonlyRootfs"] is True,
                "nonroot_config": observed["Config"]["User"] == "65534:65534",
                "network_none": host["NetworkMode"] == "none",
                "cpu_limit_config": host["NanoCpus"] == 250000000,
                "memory_limit_config": host["Memory"] == 67108864
                and host["MemorySwap"] == 67108864,
                "pids_limit_config": host["PidsLimit"] == 32,
                "capabilities_dropped": host["CapDrop"] == ["ALL"]
                and not host.get("CapAdd"),
                "no_new_privileges_config": "no-new-privileges=true"
                in host["SecurityOpt"],
                "no_privileged_or_host_namespaces": not host["Privileged"]
                and host.get("PidMode") != "host"
                and host.get("IpcMode") != "host",
                "only_disposable_readonly_bind": len(observed["Mounts"]) == 1
                and observed["Mounts"][0]["Destination"] == "/input"
                and observed["Mounts"][0]["RW"] is False,
                "no_published_ports": not host.get("PortBindings"),
                "no_host_environment_injected": observed["Config"].get("Env")
                == image["Config"].get("Env"),
            }
        )
        if not all(checks.values()):
            raise RuntimeError("Requested container controls were not applied")
        docker("start", name)
        result["events"].append("started")
        deadline = time.monotonic() + 12
        logs = ""
        while time.monotonic() < deadline:
            log_result = docker("logs", name)
            logs = log_result.stdout
            result["probe_stderr"] = log_result.stderr[:1000]
            if "ready=true" in logs:
                break
            state = json.loads(docker("inspect", name).stdout)[0]["State"]
            if not state["Running"]:
                break
            time.sleep(0.2)
        values = dict(line.split("=", 1) for line in logs.splitlines() if "=" in line)
        result["observed_inside_container"] = values
        expected = {
            "uid": "65534",
            "bind_write": "denied",
            "tmpfs_write": "allowed",
            "docker_socket": "absent",
            "cap_eff": "0000000000000000",
            "no_new_privs": "1",
            "seccomp": "2",
            "memory_max": "67108864",
            "swap_max": "0",
            "pids_max": "32",
            "cpu_max": "25000 100000",
            "interfaces": "lo",
            "external_tcp": "denied",
            "ready": "true",
        }
        checks.update(
            {
                "observed_" + key: values.get(key) == value
                for key, value in expected.items()
            }
        )
        checks["observed_readonly_root"] = values.get("root_readonly") == "true"
        checks["running_before_stop"] = json.loads(docker("inspect", name).stdout)[0][
            "State"
        ]["Running"]
        result["events"].append("stop_requested")
        started = time.monotonic()
        docker("stop", "--time", "1", name, timeout=10)
        result["stop_elapsed_seconds"] = round(time.monotonic() - started, 3)
        state = json.loads(docker("inspect", name).stdout)[0]["State"]
        result["terminal_state"] = {
            k: state[k] for k in ("Running", "ExitCode", "OOMKilled")
        }
        checks["termination_observed"] = state["Running"] is False
        checks["marker_unchanged"] = (
            hashlib.sha256(marker.read_bytes()).hexdigest() == marker_hash
        )
    except Exception as error:
        result["error_type"] = type(error).__name__
        result["error"] = str(error)[:300]
    finally:
        try:
            # Name + exact unpredictable label prove ownership even if create acknowledgement was lost.
            current = docker("inspect", name, check=False)
            if current.returncode == 0:
                owned = json.loads(current.stdout)[0]
                if (
                    owned["Config"].get("Labels", {}).get("io.faultline.preflight")
                    != scope
                ):
                    raise RuntimeError("Ownership mismatch: refusing cleanup")
                docker("rm", "-f", owned["Id"])
                result["events"].append("owned_container_removed")
            remaining = docker("ps", "-aq", "--filter", "label=" + label).stdout.split()
            all_after = set(docker("ps", "-aq", "--no-trunc").stdout.split())
            checks["cleanup_no_owned_containers"] = not remaining
            checks["preexisting_container_ids_preserved"] = before.issubset(all_after)
            result["remaining_owned_containers"] = remaining
            # Never remove a computed path outside the resolved project-local scratch directory.
            if directory.parent != local.resolve() or not directory.name.startswith(
                "docker-smoke-"
            ):
                raise RuntimeError(
                    "Scratch path is outside the approved local directory"
                )
            shutil.rmtree(directory)
            checks["cleanup_scratch_absent"] = not directory.exists()
        except Exception as error:
            result["cleanup_error_type"] = type(error).__name__
        result["status"] = (
            "PASS"
            if (
                checks
                and all(checks.values())
                and "error" not in result
                and "cleanup_error_type" not in result
            )
            else "FAIL"
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
