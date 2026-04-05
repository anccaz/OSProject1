# CS 4348 Project 1 Devlog - Annie Li

## Project Overview
**Goal:** Implement a three-process system (Driver, Logger, Encryption) using Inter-Process Communication (IPC) via pipes. The system facilitates Vigenère encryption/decryption and logs all activity with 24-hour timestamps.

---

## Log Entries

### **2026-03-06: Initial Process Architecture**
- **Task:** Creating the process hierarchy and establishing pipes.
- **Notes:** Used [fork/pipe (C) OR subprocess (Python)] to spawn the Logger and Encryption programs as children of the Driver.
- **Challenge:** The processes were terminating immediately after being spawned.
- **Solution:** Implemented a persistent `while` loop in the child programs to keep them polling `stdin` until a "QUIT" command is received.
- **OS Concept:** Verified the process tree using `ps -ef` to ensure the parent-child relationship was correctly established on the UTD servers.

### **2026-04-08: IPC Plumbing and Data Flow**
- **Task:** Redirecting Standard I/O to pipes.
- **Notes:** Established a one-way pipe for the Logger and a two-way pipe for the Encryption program.
- **Challenge:** Encountered a deadlock where the Driver would hang while waiting for a response from the Encryption program.
- **Solution:** Realized that pipes are buffered by the OS. Added explicit `fflush()` calls and ensured every command sent from the Driver ends with a newline `\n` character.
- **OS Concept:** Managing file descriptors and avoiding pipe synchronization deadlocks.

### **2026-04-10: Vigenère Engine Logic**
- **Task:** Implementing the encryption and decryption math.
- **Notes:** Coded the Vigenère shift logic: $E_i = (P_i + K_i) \mod 26$.
- **Challenge:** Ensuring case-insensitivity and handling non-alphabetical characters.
- **Solution:** Implemented a check to force all input to uppercase. Added error handling to return `ERROR` if the user attempts to encrypt/decrypt before a `PASS` (passkey) is set.

### **2026-04-12: Troubleshooting and Data Recovery**
- **Task:** Recovering files and final menu logic.
- **Notes:** Experienced an issue where source files appeared empty in VS Code. Used the "Timeline" feature to recover the code.
- **Challenge:** Implementing the history feature while maintaining security.
- **Solution:** Used a list to store encryption/decryption history. Performed a logic check to ensure that strings entered via the `password` command are sent to the Encryption process but **never** saved to the history list or the log file.

### **2026-04-13: Final Testing and Cleanup**
- **Task:** Stress testing and resource management.
- **Notes:** Verified that the Logger correctly formats timestamps as `YYYY-MM-DD HH:MM [ACTION] MESSAGE`.
- **Challenge:** Preventing "Zombie Processes" upon exiting the program.
- **Solution:** I added `wait()` calls in the Driver to ensure child processes are fully cleaned up by the OS after the "QUIT" command is issued.

---

## Technical Environment
- **Language:** [C / C++ / Python / Java]
- **Environment:** UTD CS Linux Servers (ssh)
- **Editor:** VS Code