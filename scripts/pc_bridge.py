#!/usr/bin/env python3
"""ARGOS PC Bridge — execute commands on Orion (PC) via SSH."""
import subprocess, json, sys
from pathlib import Path

PC_HOST = "192.168.1.53"
PC_USER = "AvA"
SSH_KEY = Path.home() / ".ssh/id_ed25519"

def ssh_cmd(cmd: str, timeout: int = 30) -> dict:
    """Run command on PC via SSH. Returns {ok, stdout, stderr, rc}."""
    ssh = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5",
           "-o", "PasswordAuthentication=no", f"{PC_USER}@{PC_HOST}", cmd]
    if SSH_KEY.exists():
        ssh.insert(1, "-i")
        ssh.insert(2, str(SSH_KEY))
    try:
        r = subprocess.run(ssh, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr, "rc": r.returncode}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e), "rc": -1}

def ps_check():
    r = ssh_cmd('powershell -Command "Get-WmiObject Win32_Process | Where-Object { \$_.Name -eq \'python.exe\' } | Select-Object ProcessId, CommandLine | ConvertTo-Json"')
    return r

def docker_ps():
    r = ssh_cmd('powershell -Command "docker ps --format json | ConvertTo-Json"')
    return r

def nvidia_smi():
    r = ssh_cmd("powershell -Command \"nvidia-smi --query-gpu=name,driver_version,memory.total,utilization.gpu --format=csv,noheader\"")
    return r

def mcp_health():
    r = ssh_cmd('powershell -Command "(Invoke-WebRequest -Uri http://localhost:8000/health -TimeoutSec 5).Content"')
    return r

if __name__ == "__main__":
    report = {
        "pc_ssh": ssh_cmd("whoami")["ok"],
        "nvidia": nvidia_smi()["stdout"].strip(),
        "mcp": mcp_health()["stdout"].strip(),
        "docker": docker_ps()["stdout"][:500],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
