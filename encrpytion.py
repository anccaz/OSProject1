import sys

def vigenere(text, key, encrypt=True):
    # Vigenere cipher logic: shifts letters based on the key
    result = ""
    key = key.upper()
    text = text.upper()
    
    key_index = 0
    for char in text:
        if 'A' <= char <= 'Z':
            # Calculate the shift (A=0, B=1, etc.)
            shift = ord(key[key_index % len(key)]) - ord('A')
            if not encrypt:
                shift = -shift
            
            # Perform the shift and wrap around the alphabet
            new_char_code = (ord(char) - ord('A') + shift) % 26
            result += chr(new_char_code + ord('A'))
            key_index += 1
        else:
            # According to project specs, we only process letters. 
            # Non-letters should technically be filtered by the Driver first.
            result += char
    return result

def main():
    passkey = None

    # Read commands from Driver via stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # Split command and argument (e.g., "PASS MYKEY")
        parts = line.split(" ", 1)
        command = parts[0].upper()
        argument = parts[1] if len(parts) > 1 else ""

        if command == "QUIT":
            break

        elif command == "PASS":
            passkey = argument
            print("RESULT") # Success signal to Driver

        elif command == "ENCRYPT":
            if not passkey:
                print("ERROR Password not set")
            else:
                res = vigenere(argument, passkey, encrypt=True)
                print(f"RESULT {res}")

        elif command == "DECRYPT":
            if not passkey:
                print("ERROR Password not set")
            else:
                res = vigenere(argument, passkey, encrypt=False)
                print(f"RESULT {res}")
        
        # Ensure the Driver receives the output immediately
        sys.stdout.flush()

if __name__ == "__main__":
    main()