"""يولِّد `SUSPENDED_REGISTRY.json` من شجرة `suspended/` ويفحص مطابقته — على طريقة الغانم وSLGE.

لكلّ وحدةٍ معلَّقة: مسارُها الحاليّ، مسارُها القديم، سببُ تعليقها، تاريخُه، وما يلزم لعودتها.
السببُ يُعيَّن بالمجلّد الأعلى (جدول `REASONS`)، والعودةُ بثلاثةٍ لا تتبدّل (`RE_ADMIT`).

    python tools/gen_registry.py          # يكتب السجلّ
    python tools/gen_registry.py --check  # يفشل إن خالف السجلُّ الشجرة
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUSPENDED = ROOT / "suspended"
REGISTRY = ROOT / "SUSPENDED_REGISTRY.json"
SUSPENDED_AT = "2026-10-07"

RE_ADMIT = [
    "entry and exit only through the Alghanem gate: cells come from a Certificate "
    "(src/entry.py: atoms -> cells), never from text",
    "tests with expectations independent of the code, mutation-tested (20/20 method)",
    "ADR recorded in docs/adr/",
]

REASONS = {
    "burhan": "certificate scripts reading the corpus text directly (normalize, partition, sukun…)",
    "induction": "induction engine and seals peeling text outside the gate",
    "rukhsa": "licence/ownership scripts reading text and git objects outside the gate",
    "github-workflows": "ran the suspended engines and fetched corpora; replaced by ci.yml "
    "(registry + guard + pytest)",
}
ROOT_REASON = (
    "gate/layer/engine reading text directly (algebra_engine: parse_stream falls on 22% of forms — "
    "measured; peel112/peel256 hand tables; corpus differs from the Alghanem corpus by size "
    "1,306,770 vs 1,319,901 bytes); superseded by Saleh1967/Alghanem gate/ and SLGE readers"
)
TEST_REASON = "tests of suspended modules, or expectations derived from the code under test"
SCRIPT_REASON = "shell scripts fetching/normalizing corpora outside the gate"


def entries() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for path in sorted(SUSPENDED.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(SUSPENDED)
        top = rel.parts[0]
        if len(rel.parts) == 1:
            reason = (TEST_REASON if top.startswith("test_") else SCRIPT_REASON if top.endswith(".sh")
                      else ROOT_REASON)
        else:
            reason = REASONS.get(top, "suspended pending re-admission")
        previous = ".github/workflows/" + rel.parts[-1] if top == "github-workflows" else str(rel)
        out.append(
            {
                "path": str(path.relative_to(ROOT)),
                "previous_path": previous,
                "reason": reason,
                "suspended_at": SUSPENDED_AT,
                "re_admit_requires": RE_ADMIT,
            }
        )
    return out


def render() -> str:
    body = {
        "principle": "suspension without deletion: history stays in git; "
        "nothing returns except by re_admit_requires",
        "sole_entry_exit": "Saleh1967/Alghanem gate.api (enter, exit); here only src/entry.py "
        "(certificate atoms -> cells)",
        "count": len(entries()),
        "units": entries(),
    }
    return json.dumps(body, ensure_ascii=False, indent=2) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        current = REGISTRY.read_text(encoding="utf-8") if REGISTRY.exists() else ""
        if current != text:
            print("SUSPENDED_REGISTRY.json does not match suspended/ — run tools/gen_registry.py")
            return 1
        print(f"registry matches: {len(entries())} units")
        return 0
    REGISTRY.write_text(text, encoding="utf-8")
    print(f"wrote {REGISTRY.name}: {len(entries())} units")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
