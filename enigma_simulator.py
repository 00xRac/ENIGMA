# enigma_simulator.py

from rotor_manager import load_rotor, validate_wiring, save_rotor
from enigma_core import EnigmaMachine
from utils import preprocess_message, format_output, save_to_file
from enigma_constants import ALPHABET, ENCRYPTED_FILE, DECRYPTED_FILE
import sys

# Global list to hold loaded Rotor objects
ROTORS = [None] * 3 

def load_all_rotors():
    """Attempts to load all three rotors and reports status."""
    global ROTORS
    all_ok = True
    
    for i in range(1, 4):
        rotor = load_rotor(i)
        if rotor:
            ROTORS[i-1] = rotor
        else:
            ROTORS[i-1] = None
            all_ok = False
            
    return all_ok

def get_window_setting():
    """Prompts for and validates the three-letter window setting[cite: 70]."""
    setting = input("Introdueix la posició inicial de finestra (3 lletres majúscules, p. ex. ABC): ").strip().upper()
    if len(setting) == 3 and all(c in ALPHABET for c in setting):
        return setting
    else:
        print("[ERROR] Configuració de finestra invàlida. Ha de ser 3 lletres A-Z.")
        return None

def encrypt_decrypt_option(mode):
    """Handles both encryption and decryption flow (1 and 2)."""
    
    # 1. Check for loaded rotors
    if any(r is None for r in ROTORS):
        print("[ERROR] Operació cancel·lada. Assegura't que els 3 rotors estiguin carregats i vàlids (Opció 3).")
        return
        
    window_setting = get_window_setting()
    if not window_setting:
        return

    enigma = EnigmaMachine(ROTORS)
    
    if mode == 'encrypt':
        raw_message = input("Introdueix el missatge a xifrar: ")
        processed_message = preprocess_message(raw_message)
        
        result = enigma.process_message(processed_message, window_setting, 'encrypt')
        formatted_result = format_output(result)
        
        if save_to_file(ENCRYPTED_FILE, formatted_result):
            print(f'[OK] Missatge xifrat a "{ENCRYPTED_FILE}" ({len(result)} lletres, {len(formatted_result.split())} grups de 5) [cite: 89]')
            print(f'Sortida: {formatted_result}')
            
    else: # mode == 'decrypt'
        try:
            with open(ENCRYPTED_FILE, 'r') as f:
                # Remove spaces from the Xifrat.txt content
                cipher_text = f.read().replace(' ', '')
        except FileNotFoundError:
            print(f"[ERROR] El fitxer '{ENCRYPTED_FILE}' no es troba per desxifrar. [cite: 106]")
            return

        # Decrypts the raw text (already uppercase, only A-Z)
        result = enigma.process_message(cipher_text, window_setting, 'decrypt')
        
        if save_to_file(DECRYPTED_FILE, result):
             print(f'[OK] Missatge desxifrat a "{DECRYPTED_FILE}" ({len(result)} lletres) [cite: 85, 86]')
             print(f'Sortida (sense espais): {result}')


def edit_rotors_option():
    """Allows the user to input and save a new rotor permutation[cite: 99]."""
    print("\n--- EDICIÓ DE ROTORS ---")
    try:
        rotor_index = int(input("Quin rotor vols editar? (1, 2, o 3): "))
        if rotor_index not in [1, 2, 3]:
            print("[ERROR] Índex de rotor no vàlid.")
            return
    except ValueError:
        print("[ERROR] Entrada no vàlida.")
        return
        
    new_wiring = input("Introdueix la nova permutació (26 lletres úniques A-Z): ").strip().upper()
    
    if validate_wiring(new_wiring):
        # Retrieve the old notch if the rotor was loaded, otherwise prompt
        current_rotor = ROTORS[rotor_index - 1]
        default_notch = current_rotor.notch if current_rotor else "Z"

        notch = input(f"Introdueix la lletra de notch (deixa en blanc per {default_notch}): ").strip().upper() or default_notch
        
        if save_rotor(rotor_index, new_wiring, notch):
            print(f"[OK] Rotor{rotor_index} actualitzat i guardat.")
            load_all_rotors() # Reload the updated data
    else:
        print("[ERROR] Permutació invàlida. Ha de contenir exactament 26 lletres úniques A-Z[cite: 103].")


def display_menu():
    """Displays the main interactive menu[cite: 13]."""
    print("\n=============================")
    print("      ENIGMA SIMULATOR")
    print("=============================")
    print("1. Xifrar missatge")
    print("2. Desxifrar missatge")
    print("3. Editar rotors")
    print("4. Sortir")
    print("-----------------------------")


if __name__ == "__main__":
    print("--- Càrrega inicial de rotors ---")
    if load_all_rotors():
        print("[OK] Els 3 rotors s'han carregat correctament.")
    else:
        print("[AVÍS] Hi ha errors en els rotors. Utilitza l'Opció 3 per editar i guardar-los.")
        
    while True:
        display_menu()
        choice = input("Selecciona una opció (1-4): ").strip()
        
        if choice == '1':
            encrypt_decrypt_option('encrypt') # Xifrar
        elif choice == '2':
            encrypt_decrypt_option('decrypt') # Desxifrar
        elif choice == '3':
            edit_rotors_option()
        elif choice == '4':
            print("Sortint del simulador. Adéu!")
            sys.exit(0)
        else:
            print("Opció no vàlida.")
