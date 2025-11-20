# utils.py

import re
from enigma_constants import ALPHABET, ENCRYPTED_FILE, DECRYPTED_FILE

def preprocess_message(raw_text):
    """
    Converts text to uppercase and removes non-A-Z characters (accents, spaces, signs, figures).
    """
    text = raw_text.upper()
    
    # Basic accent removal (you might need to expand this for full robustness)
    text = text.replace('À', 'A').replace('È', 'E').replace('É', 'E').replace('Í', 'I').replace('Ò', 'O').replace('Ó', 'O').replace('Ú', 'U').replace('Ü', 'U')
    
    # Remove all characters that are not A-Z
    text = re.sub(r'[^A-Z]', '', text)
    
    return text

def format_output(cipher_text):
    """
    Formats the encrypted text into groups of five letters separated by a space[cite: 81].
    """
    groups = [cipher_text[i:i + 5] for i in range(0, len(cipher_text), 5)]
    return " ".join(groups)

def save_to_file(file_name, content):
    """
    Saves the content to the specified file, handling potential errors[cite: 108].
    """
    try:
        with open(file_name, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"[ERROR] Escriptura fallida a {file_name}: {e} [cite: 108]")
        return False
