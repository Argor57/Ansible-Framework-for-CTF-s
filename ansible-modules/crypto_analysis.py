#!/usr/bin/env python3
import sys
import base64
from datetime import datetime
import re
from itertools import cycle
from string import ascii_letters
import argparse

def base64_decode(data):
    try:
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return None

def hex_decode(data):
    try:
        return bytes.fromhex(data).decode('utf-8')
    except ValueError:
        return None

def rot13_decode(data):
    return data.translate(str.maketrans(ascii_letters, ascii_letters[13:] + ascii_letters[:13]))

def frequency_analysis(data):
    filtered_data = ''.join(filter(str.isalpha, data.upper()))
    frequencies = Counter(filtered_data)
    analysis_results = "### Frequency Analysis\n"
    for letter, frequency in frequencies.most_common():
        analysis_results += f"{letter}: {frequency}\n"
    return analysis_results

def xor_with_known_plaintext(ciphertext, plaintext):
    key = ''.join(chr(c ^ p) for c, p in zip(ciphertext, cycle(plaintext)))
    potential_key = key[0]  # Assuming single-byte key for simplicity
    return potential_key

def xor_decrypt(ciphertext, key):
    decrypted = ''.join(chr(c ^ ord(key)) for c in ciphertext)
    return decrypted

def caesar_cipher_bruteforce(text):
    results = []
    for shift in range(26):
        decrypted_text = ''
        for char in text:
            if char in ascii_lowercase:
                index = (ascii_lowercase.index(char) - shift) % 26
                decrypted_text += ascii_lowercase[index]
            elif char in ascii_uppercase:
                index = (ascii_uppercase.index(char) - shift) % 26
                decrypted_text += ascii_uppercase[index]
            else:
                decrypted_text += char
        results.append(f"Shift {shift}: {decrypted_text}")
    return results

def xor_decrypt_with_known_plaintext(data, known_plaintext):
    if not known_plaintext:
        return "Known plaintext not provided, skipping XOR brute-force."
    try:
        xor_data = bytes.fromhex(data)
        potential_key = xor_with_known_plaintext(xor_data, bytes(known_plaintext, 'utf-8'))
        decrypted_xor = xor_decrypt(xor_data, potential_key)
        return f"### XOR Decryption with Potential Key '{chr(potential_key)}':\n{decrypted_xor}\n\n"
    except Exception as e:
        return f"Error during XOR decryption: {str(e)}\n\n"

def detect_and_attempt_decoding(data):
    analysis_results = "## Cryptography Analysis Results\n\n"
    
    # Attempt Base64 decoding
    base64_decoded = base64_decode(data)
    if base64_decoded:
        analysis_results += f"### Base64 Decoded Data:\n{base64_decoded}\n\n"
    
    # Attempt Hex decoding
    hex_decoded = hex_decode(data)
    if hex_decoded:
        analysis_results += f"### Hex Decoded Data:\n{hex_decoded}\n\n"
    
    # ROT13 Decoding
    analysis_results += f"### ROT13 Decoded Data:\n{rot13_decode(data)}\n\n"

    # Frequency Analysis
    analysis_results += frequency_analysis(data) + "\n"
    
    # Caesar Cipher Brute-force
    analysis_results += "### Caesar Cipher Brute-force Results\n"
    caesar_results = caesar_cipher_bruteforce(data)
    for result in caesar_results:
        analysis_results += f"{result}\n"
    
    # XOR brute-force with known plaintext
    xor_results = xor_decrypt_with_known_plaintext(data, known_plaintext)
    analysis_results += xor_results
    
    return analysis_results

def main():
    parser = argparse.ArgumentParser(description='Cryptographic Analysis Tool')
    parser.add_argument('file_path', type=str, help='Path to the file for analysis')
    parser.add_argument('--known-plaintext', type=str, help='Known plaintext for XOR brute-force', default='')
    args = parser.parse_args()

    file_path = args.file_path
    known_plaintext = args.known_plaintext

    analysis_result = detect_and_attempt_decoding(open(file_path, 'r').read().strip(), known_plaintext)
    markdown_file = save_results_to_markdown(file_path, analysis_result)
    print(markdown_file)

if __name__ == "__main__":
    main()

