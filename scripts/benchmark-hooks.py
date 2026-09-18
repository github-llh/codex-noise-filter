#!/usr/bin/env python3
"""用合成事件测量守卫开销；只写临时目录，不运行模型或用户工具。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = Path("distribution/plugin/hooks/continuity_guard.py")
sys.dont_write_bytecode = True


def measure(script: Path, iterations: int) -> dict:
    """分别统计函数快路径和完整 Python 进程，不混用两种延迟口径。"""
    spec = importlib.util.spec_from_file_location("guard_benchmark", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    payload = {"session_id": "benchmark-session", "cwd": "/synthetic/project", "model": "unchanged-model", "hook_event_name": "PostToolUse", "tool_name": "Bash", "tool_response": {"exit_code": 0, "output": "ok"}}
    with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"PLUGIN_DATA": temp}):
        module.handle_event({**payload, "hook_event_name": "SessionStart", "source": "startup"})
        state_directory = Path(temp) / "continuity"
        for index in range(60):
            (state_directory / f"synthetic-{index}.json").write_text("{}", encoding="utf-8")
        samples = []
        writes = 0
        original_save = module.save_state

        def counted_save(*args):
            nonlocal writes
            writes += 1
            return original_save(*args)

        with patch.object(module, "save_state", counted_save):
            for _ in range(iterations):
                start = time.perf_counter()
                module.handle_event(payload)
                samples.append((time.perf_counter() - start) * 1000)
        process_samples = []
        for _ in range(min(iterations, 20)):
            start = time.perf_counter()
            subprocess.run([sys.executable, str(script)], input=json.dumps(payload), text=True, capture_output=True, check=True, timeout=5)
            process_samples.append((time.perf_counter() - start) * 1000)
        return {"iterations": iterations, "state_write_calls": writes, "handler_p50_ms": round(statistics.median(samples), 3), "process_p50_ms": round(statistics.median(process_samples), 3)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", help="可选 Git ref；仅执行该已审查版本的项目守卫")
    parser.add_argument("--iterations", type=int, default=200)
    args = parser.parse_args()
    if not 1 <= args.iterations <= 10000:
        parser.error("iterations 必须在 1 到 10000 之间")
    result = {"python": platform.python_version(), "platform": platform.system(), "fixture": "successful Bash tool, unchanged model/cwd, 60 historical state files", "current": measure(ROOT / SCRIPT, args.iterations)}
    if args.baseline_ref:
        with tempfile.TemporaryDirectory() as temp:
            baseline = Path(temp) / "baseline.py"
            source = subprocess.run(["git", "show", f"{args.baseline_ref}:{SCRIPT.as_posix()}"], cwd=ROOT, capture_output=True, check=True).stdout
            baseline.write_bytes(source)
            result["baseline_ref"] = args.baseline_ref
            result["baseline"] = measure(baseline, args.iterations)
    result["scope"] = "synthetic local hook overhead only; no end-to-end latency or model-quality claim"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
