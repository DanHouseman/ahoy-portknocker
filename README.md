
# Port Knocking Script

This Python script performs port knocking, a method to access closed network ports by sending specific sequences of connection attempts to predefined ports. It supports knocking on both private and public IP addresses and checks if a target port opens after sending the sequences.

---

## Features

- **Comprehensive Port Knocking Sequences:** Contains a list of common port knock sequences.
- **Private/Public IP Detection:** Adjusts the knocking protocol based on the IP type.
- **Port Status Check:** Verifies if the target port opens after sending knock sequences.
- **Customizable:** Accepts target IP and port as command-line arguments.
- **Uses `scapy` for Packet Crafting:** Creates and sends custom TCP packets.

---

## Dependencies

The script requires the following Python libraries:
- `socket` (standard library)
- `time` (standard library)
- `ipaddress` (standard library)
- `argparse` (standard library)
- `scapy`

Install `scapy` using pip if not already installed:
```bash
pip install scapy
```

---

## Usage

### Command-Line Arguments
- `target_ip` (required): The IP address to knock on.
- `target_port` (required): The port to check after knocking.

### Example
```bash
python port_knocking.py 192.168.1.100 22
```
This example knocks on the private IP `192.168.1.100` and checks if port `22` (SSH) is open.

---

## How It Works

1. **IP Type Detection:**
   - Determines if the target IP is private or public.
   - Uses private or public IP-specific packet crafting.

2. **Knocking Sequence:**
   - Sends predefined sequences of TCP SYN packets to the target.
   - Delays 200ms between packets to simulate real-world scenarios.

3. **Port Status Check:**
   - Uses a TCP socket to verify if the target port is open.

4. **Feedback:**
   - Outputs the success or failure of each knock sequence in real-time.

---

## Code Structure

### Functions

- `is_private_ip(ip)`
  - Checks if the provided IP is private using the `ipaddress` module.

- `send_knock_sequence(target_ip, sequence, is_private)`
  - Sends a port knock sequence using TCP SYN packets.
  - Uses broadcast packets for public IPs.

- `is_port_open(target_ip, port)`
  - Checks if a specific port is open using a TCP socket.

- `main(target_ip, target_port)`
  - Orchestrates the entire knocking process:
    - Detects IP type.
    - Iterates through port knock sequences.
    - Verifies port status after each sequence.

---

## Predefined Knock Sequences

The script includes common sequences used in port knocking:

- `[7000, 8000, 9000]`
- `[12345, 23456, 34567]`
- `[22, 80, 443]`
- `[2, 3, 5, 7, 11]`
- And more...

These sequences can be easily extended or modified in the `COMMON_SEQUENCES` list.

---

## Disclaimer

This script is for educational and authorized testing purposes only. Unauthorized use on networks or systems is illegal and unethical.

---
