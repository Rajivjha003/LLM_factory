import json
import sys
from pathlib import Path
from pydantic import ValidationError

# We add the src directory to sys.path to easily import the schema
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llm_ops.data.sft_schema import SFTExample

def main():
    file_path = Path("data/sft/merchmix_sft_v1.jsonl")
    if not file_path.exists():
        print(f"File {file_path} does not exist.")
        return

    valid_count = 0
    errors = 0
    domain_counts = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                example = SFTExample(**data)
                
                domain = example.metadata.get("domain", "unknown")
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
                
                assistant_msgs = [m for m in example.messages if m.role == "assistant"]
                if not assistant_msgs:
                    print(f"Row {i} is missing an assistant message.")
                    errors += 1
                elif not assistant_msgs[-1].content.strip():
                    print(f"Row {i} has an empty assistant completion.")
                    errors += 1
                else:
                    valid_count += 1
                    
            except ValidationError as e:
                print(f"Row {i} failed schema validation: {e}")
                errors += 1
            except json.JSONDecodeError as e:
                print(f"Row {i} failed JSON parsing: {e}")
                errors += 1

    print("\n--- Validation Report ---")
    print(f"Total processed: {valid_count + errors}")
    print(f"Valid rows: {valid_count}")
    print(f"Errors: {errors}")
    
    if valid_count > 0:
        print("\nDomain Distribution:")
        for domain, count in sorted(domain_counts.items()):
            print(f"  - {domain}: {count}")

    if errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
