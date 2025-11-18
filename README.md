# Compression Bomb DOS Attack

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-educational-yellow.svg)

A comprehensive demonstration of Denial of Service (DOS) attacks using compression bombs against vulnerable file processing services. This project was created for **CY5150 - Systems Security** at Northeastern University to demonstrate the critical importance of input validation in web applications.

---

## **LEGAL DISCLAIMER**

**FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY**

This project demonstrates security vulnerabilities in file processing systems for educational purposes. **Unauthorized use of these tools is illegal and unethical.**

### **Permitted Use:**
- Educational environments and coursework
- Authorized penetration testing with written permission
- Security research in controlled lab environments
- Testing on systems you own

### **Prohibited Use:**
- Unauthorized attacks on production systems
- Testing without explicit written permission
- Any malicious or illegal activity
- Attacks against systems you do not own

**By downloading or using this code, you agree to:**
1. Use it only for lawful, educational purposes
2. Only test on systems you own or have explicit written authorization to test
3. Accept full legal responsibility for your actions
4. Acknowledge that the author is not responsible for any misuse

**VIOLATION OF THESE TERMS MAY RESULT IN:**
- Criminal prosecution under the Computer Fraud and Abuse Act (CFAA)
- Civil liability for damages
- Academic sanctions
- Permanent legal consequences

**The author disclaims all liability for misuse of this software.**

---

## Overview

This project demonstrates how **improperly validated file uploads** can lead to complete service denial through resource exhaustion. Four different compression bomb variants were created and tested against a vulnerable Flask application, achieving sustained Denial of Service through disk space and memory exhaustion.

### What is a Compression Bomb?

A **compression bomb** (also known as a "zip bomb" or "decompression bomb") is a malicious archive file designed to crash or render useless the program or system reading it. These files are small when compressed but expand to enormous sizes when decompressed, overwhelming system resources.

**Classic Example:** The infamous `42.zip` file is only 42 kilobytes compressed but expands to 4.5 petabytes when fully extracted.

## Architecture
```
┌─────────────────────────┐         ┌─────────────────────────┐
│  Machine 1: Attacker    │────────>│  Machine 2: Target      │
│  (WSL/Linux/macOS)      │  HTTP   │  (Kali VM)              │
│                         │  POST   │                         │
│  • Bomb Generator       │ (Port   │  • Vulnerable Flask     │
│  • Attack Scripts       │  5000)  │  • Limited Resources    │
│  • Monitoring Tools     │         │  • Resource Monitor     │
└─────────────────────────┘         └─────────────────────────┘
```
        
Network: 192.168.56.x/24 (Host-Only or NAT)
Protocol: HTTP POST with multipart/form-data
Payload: Malicious ZIP files


## Machine 1:
# Clone repository
git clone https://github.com/ahmedsnaj30/Compression_Bomb.git
cd Compression_Bomb

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
./setup.sh

# Pause Here

## Machine 2:
sudo apt update
sudo apt install python3 python3-pip python3-flask python3-psutil -y

# Copy vuln_service.py to this machine and start vulnerable service
python3 vuln_service.py


## Machine 1:
# Launch Attack
python3 remote_attack.py <Machine 2 IP>


