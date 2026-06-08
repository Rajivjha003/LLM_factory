import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    rows = read_jsonl(args.eval_jsonl)

    near_pass = [
        row for row in rows
        if not row.get("passed", False) and float(row.get("score_rate", 0.0)) >= 0.90
    ]

    lines = [
        "# Judge v2 Near-Pass Audit",
        "",
        f"Eval file: `{args.eval_jsonl}`",
        f"Total rows: {len(rows)}",
        f"Near-pass rows (Score >= 0.90 but Failed): {len(near_pass)}",
        ""
    ]

    for idx, row in enumerate(near_pass, start=1):
        lines.append(f"## {idx}. {row.get('id')}")
        lines.append(f"**Score Rate:** {row.get('score_rate'):.3f}")
        lines.append("")
        lines.append("### Missing Required Terms")
        missing = row.get("missing_required", [])
        if missing:
            lines.append(f"`{missing}`")
        else:
            lines.append("None")
        lines.append("")
        
        lines.append("### Feedback")
        feedback = row.get("feedback", [])
        for fb in feedback:
            lines.append(f"- {fb}")
        lines.append("")
        
        lines.append("### Model Response")
        lines.append("```text")
        lines.append(row.get("response", ""))
        lines.append("```")
        lines.append("---")
        lines.append("")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Found {len(near_pass)} near-pass cases.")
    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
