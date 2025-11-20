# rotor_manager.py
from enigma_constants import ALPHABET, ROTOR_FILES

class Rotor:
    """Represents a single Enigma rotor with its wiring, notch, and current position."""
    def __init__(self, index, wiring, notch="Z"):
        self.index = index  # 1, 2, or 3
        self.wiring = wiring
        self.notch = notch.upper()
        self.position = 0  # Current rotational offset (0-25)

def validate_wiring(wiring):
    """
    Checks if the wiring is a valid permutation of the 26 letters (A-Z)[cite: 103].
    """
    if len(wiring) != 26:
        return False
    # Check if all characters are unique and uppercase A-Z
    if set(wiring) != set(ALPHABET):
        return False
    
    return True

def get_inverse_wiring(wiring):
    """
    Calculates the inverse mapping of the rotor wiring, needed for decryption[cite: 56].
    """
    inverse = [''] * 26
    for i, char in enumerate(wiring):
        # char is the output letter, i is the input index (0=A, 1=B, etc.)
        output_index = ALPHABET.index(char)
        inverse[output_index] = ALPHABET[i]
        
    return "".join(inverse)

def load_rotor(rotor_index):
    """
    Loads wiring and notch from RotorX.txt[cite: 62].
    Returns a Rotor object or None if invalid/error.
    """
    file_name = ROTOR_FILES[rotor_index - 1]
    
    try:
        with open(file_name, 'r') as f:
            lines = [line.strip().upper() for line in f.readlines()]
            
            wiring = lines[0] if len(lines) > 0 else ""
            # Notch defaults to 'Z' if the second line is omitted [cite: 68]
            notch = lines[1] if len(lines) > 1 and lines[1] else "Z" 
            
            if not validate_wiring(wiring):
                print(f"[ERROR] {file_name}: permutació incorrecta - calen 26 lletres úniques A-Z [cite: 90, 91]")
                return None
                
            return Rotor(rotor_index, wiring, notch)

    except FileNotFoundError:
        print(f"[ERROR] El fitxer {file_name} no existeix. [cite: 106]")
        return None
    except Exception as e:
        print(f"[ERROR] Lectura o escriptura fallida de {file_name}: {e} [cite: 108]")
        return None

def save_rotor(rotor_index, wiring, notch):
    """Saves the rotor configuration to its file."""
    file_name = ROTOR_FILES[rotor_index - 1]
    try:
        with open(file_name, 'w') as f:
            f.write(wiring + '\n')
            f.write(notch + '\n')
        return True
    except Exception as e:
        print(f"[ERROR] Escriptura fallida a {file_name}: {e} [cite: 108]")
        return False
