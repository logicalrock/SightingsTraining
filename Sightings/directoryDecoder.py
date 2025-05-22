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

# Load the same 2048-word wordlist used during encoding
with open('wordlist.txt', 'r') as f:
    WORDLIST = [line.strip() for line in f.readlines()]
assert len(WORDLIST) == 2048, "Wordlist must contain exactly 2048 words."

# Build reverse lookup dictionary
WORD_INDEX = {word: idx for idx, word in enumerate(WORDLIST)}

def decode_file(encoded_path='policyReenforcement.txt', output_base='reconstructed'):
    with open(encoded_path, 'r') as f:
        lines = f.read().splitlines()

    i = 0
    while i < len(lines):
        if lines[i].startswith("::FILE_START::"):
            rel_path = lines[i].split("::FILE_START::")[1]
            i += 1
            encoded_words = []
            while i < len(lines) and not lines[i].startswith("::FILE_END::"):
                encoded_words.extend(lines[i].split())
                i += 1

            # Convert words back to bit string
            bit_string = ''.join(f'{WORD_INDEX[word]:011b}' for word in encoded_words)

            # Split into bytes
            byte_chunks = [bit_string[j:j+8] for j in range(0, len(bit_string), 8)]
            byte_data = bytes([int(b, 2) for b in byte_chunks if len(b) == 8])

            # Write to reconstructed file
            output_path = os.path.join(output_base, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f_out:
                f_out.write(byte_data)

        i += 1

    print(f"All files reconstructed in '{output_base}/'")

if __name__ == "__main__":
    decode_file()
