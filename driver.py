import subprocess
import sys

def log_event(log_pipe, action, message):
    # Sends a message to the logger process
    log_pipe.stdin.write(f"{action} {message}\n")
    log_pipe.stdin.flush()

def is_valid(s):
    # Requirements specify only letters are allowed (no spaces or symbols)
    return s.isalpha()

def get_input_choice(history):
    # Helper to let user choose between new string or history
    if not history:
        return input("Enter string: ")
    
    print("\nOptions: (1) Enter new string (2) Select from history")
    choice = input("Choice: ")
    
    if choice == "2":
        print("\nHistory:")
        for i, item in enumerate(history):
            print(f"{i}: {item}")
        idx = input("Select number (or 'x' to cancel): ")
        if idx.lower() == 'x':
            return None
        try:
            return history[int(idx)]
        except:
            print("Invalid selection.")
            return None
    else:
        val = input("Enter new string: ")
        if is_valid(val):
            return val
        print("ERROR: Only letters allowed.")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 driver.py <log_file>")
        return

    log_file = sys.argv[1]
    history = []

    # 1. Start child processes with pipes
    # text=True handles strings instead of bytes
    logger = subprocess.Popen(['python3', 'logger.py', log_file], 
                              stdin=subprocess.PIPE, text=True)
    
    encryptor = subprocess.Popen(['python3', 'encryption.py'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, text=True)

    log_event(logger, "START", "Driver program started")

    while True:
        print("\n--- MENU ---")
        print("1. password\n2. encrypt\n3. decrypt\n4. history\n5. quit")
        choice = input("Select an option: ").strip().lower()

        if choice == "5" or choice == "quit":
            log_event(logger, "QUIT", "User quit")
            encryptor.stdin.write("QUIT\n")
            encryptor.stdin.flush()
            logger.stdin.write("QUIT\n")
            logger.stdin.flush()
            break

        elif choice == "4" or choice == "history":
            print("\n--- History ---")
            for item in history:
                print(item)

        elif choice in ["1", "2", "3", "password", "encrypt", "decrypt"]:
            # Map numbers to commands
            cmd_map = {"1": "password", "2": "encrypt", "3": "decrypt"}
            cmd_type = cmd_map.get(choice, choice)

            target_str = get_input_choice(history)
            if not target_str:
                continue

            # Command to send to encryption.py
            cmd_to_send = "PASS" if cmd_type == "password" else cmd_type.upper()
            
            # LOGGING: Record the action (Hide password content)
            log_msg = "********" if cmd_type == "password" else target_str
            log_event(logger, cmd_to_send, log_msg)

            # COMMUNICATE with encryption.py
            encryptor.stdin.write(f"{cmd_to_send} {target_str}\n")
            encryptor.stdin.flush()
            
            # Get result from encryption.py
            result = encryptor.stdout.readline().strip()
            print(f"Response: {result}")
            
            # LOGGING: Record the result
            log_event(logger, "RESULT", result)

            # Update history (don't store passwords or error messages)
            if "RESULT" in result:
                if cmd_type != "password":
                    if target_str not in history: history.append(target_str)
                    res_val = result.replace("RESULT ", "")
                    if res_val not in history: history.append(res_val)

    # Wait for children to finish
    encryptor.wait()
    logger.wait()
    print("System shut down gracefully.")

if __name__ == "__main__":
    main()