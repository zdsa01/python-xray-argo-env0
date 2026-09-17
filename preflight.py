#!/usr/bin/env python3
"""Lightweight preflight checks for CI/env0 repositories without requiring Helm."""
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parent
required = [
    root / "Chart.yaml",
    root / "values.yaml",
    root / "templates" / "deployment.yaml",
    root / "templates" / "service.yaml",
    root / "templates" / "secret.yaml",
]
missing = [str(p.relative_to(root)) for p in required if not p.is_file()]
if missing:
    print("Missing chart files:", ", ".join(missing), file=sys.stderr)
    raise SystemExit(1)

chart = (root / "Chart.yaml").read_text(encoding="utf-8")
values = (root / "values.yaml").read_text(encoding="utf-8")
for needle in ("apiVersion: v2", "name: python-xray-argo"):
    if needle not in chart:
        print(f"Chart.yaml missing {needle!r}", file=sys.stderr)
        raise SystemExit(1)
for needle in ("image:", "service:", "secretEnv:", "env:"):
    if needle not in values:
        print(f"values.yaml missing {needle!r}", file=sys.stderr)
        raise SystemExit(1)

dep = (root / "templates" / "deployment.yaml").read_text(encoding="utf-8")
if "imagePullSecrets:\n{{- with .Values.imagePullSecrets }}" in dep:
    print("imagePullSecrets conditional placement is invalid", file=sys.stderr)
    raise SystemExit(1)
print("env0 Helm preflight: OK")
