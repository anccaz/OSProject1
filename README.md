# Project 1: Vigenère Cipher IPC System

## Overview
This project implements a multi-process encryption system using **Inter-Process Communication (IPC)**. It consists of a central driver that manages two child processes via pipes: a backend encryption engine and a centralized logging service.



## System Architecture

The project is divided into three functional modules:

1. **Driver (`driver.py`)**: 
   - The "Master" process.
   - Manages the lifecycle of child processes using the `subprocess` module.
   - Handles the interactive User Interface and maintains an operation history.
   - Routes data between the user, the encryptor, and the logger.

2. **Encryption Engine (`encryption.py`)**:
   - A standalone service that implements the Vigenère cipher.
   - Maintains the state of the current passkey.
   - Communicates exclusively through `stdin` (input commands) and `stdout` (results).

3. **Logger (`logger.py`)**:
   - A dedicated process for file I/O.
   - Appends timestamped events to a log file in the format: `YYYY-MM-DD HH:MM [ACTION] MESSAGE`.



## Requirements
- **Language**: Python 3.x
- **Libraries**: `subprocess`, `sys`, `datetime`
- **Operating System**: macOS (Terminal), Linux, or Windows with Python 3 installed.

## Features
- **Secure Logging**: Passwords are redacted in the logs (displayed as `********`).
- **Input Validation**: The system strictly enforces "letters only" for passwords and cryptographic strings, preventing invalid characters from being processed.
- **Case Insensitivity**: The Vigenère logic treats "ABC" and "abc" identically.
- **History Management**: Allows users to select previous inputs or results to perform further operations without re-typing.

## Setup and Installation

1. **Initialize the environment**:
   ```bash
   mkdir OS_Project1
   cd OS_Project1
   git init