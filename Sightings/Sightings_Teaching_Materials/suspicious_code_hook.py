# suspicious_code_hook.py
# Hook script to flag suspicious patterns during commit or pipeline execution

import os
import sys
import re

def scan_file(file_path):
    flags = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

        if 'os.walk' in content and 'open(' in content:
            flags.append("⚠️ Recursive file access detected.")

        if re.search(r'\b(bitstring|08b|11b|set|dict)\b', content):
            flags.append("⚠️ Bit-level manipulation or unusual data structure use.")

        if 'def main(' in content and '--' in content:
            flags.append("⚠️ Flag-based dual execution paths.")

        if 'policyReenforcement' in content or 'sightings_log' in content:
            flags.append("⚠️ Suspicious file naming detected.")

        if 'anomaly' in content and 'log' in content:
            flags.append("⚠️ Misdirection pattern: fake anomaly logging.")

    return flags

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sightings.py"
    if not os.path.exists(target):
        print(f"File {target} not found.")
        sys.exit(1)

    issues = scan_file(target)
    if issues:
        print(f"🔍 Suspicious patterns found in {target}:")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print(f"✅ No suspicious patterns detected in {target}")
        sys.exit(0)
