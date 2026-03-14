import subprocess
import sys

def log_event(pipe, action, message):
    pipe.stdin.write(f"{action} {message}\n")
    pipe.stdin.flush()

def is_valid(s):
    return s.isalpha() # Only letters allowed [cite: 91]

def main():
    if len(sys.argv) < 2:
        print("Usage: python driver.py <log_file>")
        return

    log_file = sys.argv[1]
    history = [] # Temporary history [cite: 67]

    # Launch sub-processes [cite: 60]
    logger = subprocess.Popen(['python3', 'logger.py', log_file], stdin=subprocess.PIPE, text=True)
    encryptor = subprocess.Popen(['python3', 'encryption.py'], stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, text=True)

    log_event(logger, "START", "Driver program started") [cite: 66]

    while True:
        print("\nCommands: password, encrypt, decrypt, history, quit")
        choice = input("Enter command: ").strip().lower()

        if choice == "quit":
            log_event(logger, "QUIT", "User quit") [cite: 87]
            encryptor.stdin.write("QUIT\n") [cite: 87]
            logger.stdin.write("QUIT\n") [cite: 87]
            break

        elif choice == "history":
            print("History:")
            for i, item in enumerate(history):
                print(f"{i}: {item}") [cite: 86]

        elif choice in ["password", "encrypt", "decrypt"]:
            target_str = ""
            
            # History selection logic [cite: 69, 73, 82]
            if history and input("Use history? (y/n): ").lower() == 'y':
                for i, item in enumerate(history): print(f"{i}: {item}")
                idx = input("Select number (or 'x' to cancel): ")
                if idx == 'x': continue
                target_str = history[int(idx)]
            else:
                target_str = input(f"Enter string for {choice}: ")
                if not is_valid(target_str):
                    print("ERROR: Only letters allowed") [cite: 92]
                    continue
                if choice != "password": history.append(target_str)

            # Communicate with encryption backend
            cmd = "PASS" if choice == "password" else choice.upper()
            log_event(logger, cmd, target_str if choice != "password" else "********") [cite: 89]
            
            encryptor.stdin.write(f"{cmd} {target_str}\n")
            encryptor.stdin.flush()
            
            result = encryptor.stdout.readline().strip()
            print(result)
            log_event(logger, "RESULT", result) [cite: 65]
            
            if "RESULT" in result and choice != "password":
                res_parts = result.split(" ", 1)
                if len(res_parts) > 1: history.append(res_parts[1]) [cite: 76, 85]

    encryptor.wait()
    logger.wait()

if __name__ == "__main__":
    main()