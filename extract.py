import re
import os

with open('/home/rajiv/LLM_Ops/pre_phase_fix.txt', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.finditer(r'touch (\S+).*?Paste:.*?```(?:python|bash|text)\n(.*?)```\n', text, re.DOTALL)
for match in matches:
    filename = match.group(1).strip()
    content = match.group(2)
    filepath = f"/home/rajiv/LLM_Ops/{filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    print(f"Writing {filename}...")
    with open(filepath, 'w', encoding='utf-8') as out:
        out.write(content)

os.system("chmod +x /home/rajiv/LLM_Ops/scripts/phase45_truth_audit.sh")
