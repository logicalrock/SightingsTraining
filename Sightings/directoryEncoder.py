'''
Objective Summary:
Input: A file (any type, binary or text).

Output: A completely different, human-readable file made up of dictionary words, representing the original file in an obfuscated way.

Reversibility: The process must allow bit-for-bit exact reconstruction of the original file from the obfuscated form.

Randomness: The obfuscated format must not resemble the original file at all and must vary per encoding.

Human-readable disguise: The output should appear as a plausible “text” file with logical dictionary words — like a story, paragraph, or list of words.

How This Can Be Done:
This is a form of dictionary-based binary encoding. Here’s one approach:
'''
'''
Two-Script System Overview:

Part 1: encode_file_to_words.py

Determine current directory.
Go up 2 levels (if possible).
From each of those (up to 3) directories (current + 2 parents), scan up to 2 subdirectory levels deep.
Read all files found.
Encode everything (even mixed file types) into a single encoded .txt using the same bit-chunk to dictionary-word method.
'''
'''
Part 2: decode_words_to_file.py

Read the encoded word list.
Map each word back to its corresponding bit chunk.
Reconstruct the bitstream.
Write it back as binary, identical to the original file.
'''
'''
Why This Works
This is similar to Base64 or Diceware encoding but uses dictionary words instead of symbols. It's lossless and reversible, but obfuscated and human-readable.
'''
'''
Wordlist Example (wordlist.txt)
You need a dictionary file with 2048 unique words. You can use:

EFF Diceware wordlist: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt (trim to 2048 entries)

Or I can generate one for you if needed.
'''
'''
Test Run
Save your file as original_file.any

Run encode_file_to_words.py

Transfer encoded_words.txt anywhere (human-readable, safe to email, etc.)

On the receiving side, run decode_words_to_file.py to recover the original bit-for-bit file.
'''

import os

# Load wordlist (must be exactly 2048 words)
with open('wordlist.txt', 'r') as f:
    WORDLIST = [line.strip() for line in f.readlines()]
assert len(WORDLIST) == 2048, "Wordlist must contain exactly 2048 words."

def get_scan_dirs(start_dir, up=2, down=2):
    dirs_to_scan = set()

    current = start_dir
    for _ in range(up + 1):
        if os.path.isdir(current):
            dirs_to_scan.add(current)
        current = os.path.dirname(current)

    final_dirs = set()
    for d in dirs_to_scan:
        for root, dirs, files in os.walk(d):
            rel_depth = os.path.relpath(root, d).count(os.sep)
            if rel_depth <= down:
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
                    bits = ''.join(f'{byte:08b}' for byte in binary)
                    chunks = [bits[i:i+11] for i in range(0, len(bits), 11)]
                    if len(chunks[-1]) < 11:
                        chunks[-1] = chunks[-1].ljust(11, '0')

                    words = [WORDLIST[int(chunk, 2)] for chunk in chunks]

                    encoded_output.append(f"::FILE_START::{rel_path}")
                    encoded_output.append(' '.join(words))
                    encoded_output.append("::FILE_END::\n")

                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

    with open(output_path, 'w') as f:
        f.write('\n'.join(encoded_output))

    print(f"Encoding complete. Output written to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))
    dirs = get_scan_dirs(base_dir, up=2, down=2)
    encode_files(dirs)
