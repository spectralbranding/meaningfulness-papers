"""Validate all L3 JSONL session records against session_record.schema.json.

Usage:
    uv run python experiment/validation/validate.py
    uv run python experiment/validation/validate.py --logs-dir logs/

Exit 0 on all records passing validation.
Exit 1 on any validation failures (details printed to stdout).

Optional pre-commit hook note:
    Add to .git/hooks/pre-commit (do not install automatically):
        uv run python research/meaning-meaningfulness-empirical/experiment/validation/validate.py
    This is a suggestion only; the hook is not installed by this script.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_schema(schema_path: Path) -> dict:
    with schema_path.open() as f:
        return json.load(f)


def validate_record(record: dict, schema: dict, required: list[str]) -> list[str]:
    """Return list of violation strings; empty = valid."""
    violations = []
    for field in required:
        if field not in record:
            violations.append(f"Missing required field: '{field}'")
    return violations


def main(logs_dir: Path) -> int:
    schema_path = Path(__file__).parent / "session_record.schema.json"
    if not schema_path.exists():
        print(f"ERROR: schema not found at {schema_path}", file=sys.stderr)
        return 2

    schema = load_schema(schema_path)
    required_fields: list[str] = schema.get("required", [])

    jsonl_files = sorted(logs_dir.glob("*.jsonl"))
    if not jsonl_files:
        print(f"No .jsonl files found in {logs_dir}")
        return 0

    total_records = 0
    total_failures = 0

    for jsonl_path in jsonl_files:
        file_failures = 0
        try:
            lines = jsonl_path.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            print(f"ERROR reading {jsonl_path.name}: {e}")
            total_failures += 1
            continue

        for line_no, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"FAIL  {jsonl_path.name}:{line_no}  JSON parse error: {e}")
                file_failures += 1
                total_failures += 1
                total_records += 1
                continue

            violations = validate_record(record, schema, required_fields)
            total_records += 1
            if violations:
                for v in violations:
                    print(f"FAIL  {jsonl_path.name}:{line_no}  {v}")
                file_failures += 1
                total_failures += 1
            # else: pass silently

        if file_failures == 0:
            valid_count = len([l for l in lines if l.strip()])
            print(f"PASS  {jsonl_path.name}  ({valid_count} records)")

    print(f"\nTotal: {total_records} records across {len(jsonl_files)} files — "
          f"{total_failures} failures, {total_records - total_failures} passed.")

    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate L3 JSONL session records.")
    parser.add_argument(
        "--logs-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "logs",
        help="Directory containing .jsonl log files (default: ../../logs/)",
    )
    args = parser.parse_args()
    sys.exit(main(args.logs_dir))
