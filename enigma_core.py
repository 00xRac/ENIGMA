# enigma_core.py

from enigma_constants import ALPHABET
from rotor_manager import Rotor, get_inverse_wiring

class EnigmaMachine:
    """
    Simulates the core electromechanical behavior of the Enigma machine (rotor stepping and transformation).
    """
    def __init__(self, rotors: list[Rotor]):
        # Rotors are expected in order: R1 (Fast), R2 (Middle), R3 (Slow)
        self.rotors = rotors
        
    def set_positions(self, window_setting):
        """Sets the initial position of the rotors based on the window setting (e.g., 'A', 'C', 'B')[cite: 70, 71]."""
        for i, char in enumerate(window_setting):
            self.rotors[i].position = ALPHABET.index(char)
        
    def rotor_advance(self):
        """
        Implements the rotor stepping mechanism (odometer effect + notch)[cite: 96, 97].
        """
        
        # Get notch indices for R1 and R2
        r1_notch_idx = ALPHABET.index(self.rotors[0].notch)
        r2_notch_idx = ALPHABET.index(self.rotors[1].notch)
        
        r1_pos = self.rotors[0].position
        r2_pos = self.rotors[1].position

        # --- Stepping Logic (Double Stepping implemented) ---

        # 1. R2 to R3 Carry: If R2 is at its notch position
        step_r3 = (r2_pos == r2_notch_idx) 

        # 2. R1 to R2 Carry: If R1 is at its notch OR R2 is carrying to R3 (Double Stepping)
        step_r2 = (r1_pos == r1_notch_idx) or step_r3 

        # --- ADVANCE ROTORS ---
        
        # Always advance R1 (Fast wheel) [cite: 96]
        self.rotors[0].position = (r1_pos + 1) % 26
        
        # Advance R2
        if step_r2:
            self.rotors[1].position = (r2_pos + 1) % 26
            
        # Advance R3
        if step_r3:
            self.rotors[2].position = (self.rotors[2].position + 1) % 26
            
    def transform_letter(self, char, direction='encrypt'):
        """
        Passes a single letter through the rotors[cite: 33].
        For this simulation, the transformation is a one-way trip through the rotors
        (R1->R2->R3) for encryption, and the inverse for decryption (R3->R2->R1 inverse)[cite: 56].
        """
        current_index = ALPHABET.index(char)
        
        # Define the path based on direction
        if direction == 'encrypt':
            # Path: R1 -> R2 -> R3
            rotor_order = [0, 1, 2] 
            use_inverse = False
        else: # 'decrypt'
            # Path: R3(Inverse) -> R2(Inverse) -> R1(Inverse)
            rotor_order = [2, 1, 0] # Order is reversed
            use_inverse = True

        for i in rotor_order:
            rotor = self.rotors[i]
            
            # Determine wiring to use
            if use_inverse:
                wiring = get_inverse_wiring(rotor.wiring)
            else:
                wiring = rotor.wiring

            # 1. Apply forward rotation offset (input contact to internal wiring index)
            shifted_index = (current_index + rotor.position) % 26
            
            # 2. Pass through the wiring (transformation)
            transformed_char = wiring[shifted_index]
            transformed_index = ALPHABET.index(transformed_char)
            
            # 3. Apply backward rotation offset (internal wiring index to output contact)
            current_index = (transformed_index - rotor.position) % 26
            
        return ALPHABET[current_index]

    def process_message(self, message, window_setting, direction='encrypt'):
        """Encrypts or decrypts a message letter by letter."""
        self.set_positions(window_setting)
        output_chars = []
        
        # We process the already preprocessed message (only A-Z)
        for char in message:
            self.rotor_advance() # Advance rotors *before* transforming the letter [cite: 30]
            transformed_char = self.transform_letter(char, direction)
            output_chars.append(transformed_char)
            
        return "".join(output_chars)
