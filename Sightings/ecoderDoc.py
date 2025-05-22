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
Read the input file in binary.

Convert to base64 or direct bitstring.

Break bitstream into fixed-size chunks (e.g. 11 bits gives 2048 options).

Map each chunk to a word from a large dictionary of ~2048 words (like EFF's Diceware wordlist).

Output a .txt file with the encoded words.
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

# Encoder

import os
import sys
import base64
import math
import random

# Load a dictionary of exactly 2048 unique words
with open('wordlist.txt', 'r') as f:
    WORDLIST = [line.strip() for line in f.readlines()]
assert len(WORDLIST) == 2048, "Wordlist must contain exactly 2048 words."

def file_to_wordlist(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    bit_string = ''.join(f'{byte:08b}' for byte in data)
    chunks = [bit_string[i:i+11] for i in range(0, len(bit_string), 11)]

    # Pad last chunk if needed
    if len(chunks[-1]) < 11:
        chunks[-1] = chunks[-1].ljust(11, '0')

    words = [WORDLIST[int(chunk, 2)] for chunk in chunks]

    # Save output
    with open(output_path, 'w') as f:
        f.write(' '.join(words))

    print(f"Encoded to {output_path}")

if __name__ == "__main__":
    file_to_wordlist('original_file.any', 'encoded_words.txt')
