#!/usr/bin/env python3
"""Confirm every model identifier in PROTOCOL.yaml answers, before the run spends anything.

One trivial call per role. The predecessor's protocol had to correct a served
identifier during its pilot; doing that here after 150 extraction calls had
started would mean discarding them.

Run:
    bws run -- uv run --with httpx --with pyyaml python \\
        code/smoke_models.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import unit_lib as L  # noqa: E402


def main() -> int:
    proto = L.protocol()
    roles = [("operator", o) for o in proto["extraction_operators"]]
    roles.append(("unitizer", proto["unitizer"]))
    roles += [("adjudicator", a) for a in proto["segmentation_adjudicators"]]
    roles.append(("resolver", proto["adjudication_resolver"]))

    bad = 0
    for role, spec in roles:
        try:
            text = L.call_model(
                spec["model"],
                spec["family"],
                'Reply with the single JSON object {"ok": true} and nothing else.',
                "Reply now.",
                role=f"smoke_{role}",
                operation=f"smoke|{spec['id']}",
                phase="unitization_smoke",
                max_out=2000,
            )
            ok = L.parse_json_block(text).get("ok")
            print(
                f"  {spec['id']:6s} {role:12s} {spec['family']:10s} {spec['model']:28s} OK ({ok})"
            )
        except Exception as exc:  # noqa: BLE001 -- the point is to see which fail
            bad += 1
            print(
                f"  {spec['id']:6s} {role:12s} {spec['family']:10s} {spec['model']:28s} FAILED {type(exc).__name__}: {str(exc)[:160]}"
            )
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
