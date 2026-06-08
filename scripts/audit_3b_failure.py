import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-jsonl", type=Path, required=True)
    parser.add_argument("--training-report", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    training_report = read_json(args.training_report)
    
    # Try to find a trainer_state.json in the parent directory's checkpoint folders
    trainer_state_path = None
    adapter_dir = args.training_report.parent
    if adapter_dir.exists() and adapter_dir.is_dir():
        for cp in adapter_dir.glob("checkpoint-*"):
            ts = cp / "trainer_state.json"
            if ts.exists():
                trainer_state_path = ts
                break
                
    trainer_state = read_json(trainer_state_path) if trainer_state_path else {}

    rows = []
    if args.eval_jsonl.exists():
        with args.eval_jsonl.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))

    lines = [
        "# 3B QLoRA Failure Audit",
        "",
        "## 1. Training Diagnostics",
    ]

    if not training_report:
        lines.append("`phase5_training_metadata.json` not found.")
    else:
        lines.append("```json")
        lines.append(json.dumps(training_report, indent=2))
        lines.append("```")
        
        history = trainer_state.get("log_history", [])
        if not history:
            lines.append("**Status:** Unknown (No loss history found in checkpoints)")
        else:
            first_loss = history[0].get("loss", 0.0)
            last_loss = history[-1].get("loss", 0.0)
            lines.append(f"**First Loss:** {first_loss:.4f}")
            lines.append(f"**Final Loss:** {last_loss:.4f}")
            if last_loss > first_loss:
                lines.append("**Conclusion:** Loss exploded or failed to converge. This indicates a bad hyperparameter or target module config.")
            elif last_loss > 0.5:
                lines.append("**Conclusion:** Loss decreased but remained high. Model failed to fit the data.")
            else:
                lines.append("**Conclusion:** Loss converged normally (final loss < 0.5). The training mechanics worked, meaning the failure is likely related to adapter loading, chat templates, or the 3B model's inherent instruction-following characteristics.")
                
            # Adapter file checks
            st_path = adapter_dir / "adapter_model.safetensors"
            if st_path.exists():
                size_mb = st_path.stat().st_size / (1024 * 1024)
                lines.append(f"**Adapter Size:** {size_mb:.2f} MB")
                if size_mb < 10:
                    lines.append("**Conclusion:** Adapter size is suspiciously small! Target modules might be wrong.")
                else:
                    lines.append("**Conclusion:** Adapter size is reasonable for 3B.")
            else:
                lines.append("**Conclusion:** `adapter_model.safetensors` NOT FOUND!")

    lines.extend([
        "",
        "## 2. Evaluation Diagnostics"
    ])

    if not rows:
        lines.append("No evaluation rows found.")
    else:
        avg_score = sum(r.get("score_rate_v2", r.get("score_rate", 0.0)) for r in rows) / len(rows)
        avg_length = sum(len(r.get("response", "")) for r in rows) / len(rows)
        passed_count = sum(1 for r in rows if r.get("passed_v2", r.get("passed", False)))
        
        lines.append(f"- **Total Rows:** {len(rows)}")
        lines.append(f"- **Pass Rate:** {passed_count / len(rows):.2%}")
        lines.append(f"- **Average Score Rate:** {avg_score:.2f}")
        lines.append(f"- **Average Response Length:** {avg_length:.0f} chars")
        lines.append("")
        
        # Check verbosity
        if avg_length > 1000:
            lines.append("**Conclusion:** The model is extremely verbose (>1000 chars/response). This often triggers forbidden term false-positives or format breakages.")
        elif avg_length < 50:
            lines.append("**Conclusion:** The model is producing empty or near-empty responses. This strongly suggests the adapter is broken, the EOS token is broken, or the prompt template is mismatched.")
        else:
            lines.append("**Conclusion:** Response length is normal. The failure might be hallucination, poor instruction following, or an adapter that was not loaded correctly during inference.")

        # Show 3 random responses
        lines.append("")
        lines.append("### Sample Outputs")
        for i, row in enumerate(rows[:5], start=1):
            lines.append(f"**Sample {i} ({row.get('id')}):**")
            lines.append("```text")
            lines.append(row.get("response", "").strip()[:500] + " ... [truncated]")
            lines.append("```")
            lines.append("")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
