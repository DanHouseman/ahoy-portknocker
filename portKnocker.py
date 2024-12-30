import socket
import time
import ipaddress
import argparse
from scapy.all import IP, TCP, send, Ether

# List of common port knock sequences
COMMON_SEQUENCES = [
    [7000, 8000, 9000],
    [12345, 23456, 34567],
    [22, 80, 443],
    [1111, 2222, 3333],
    [8080, 9090, 10000],
    [21, 22, 23],
    [1194, 500, 1701],
    [25, 110, 143],
    [49152, 49153, 49154],
    [1357, 2468, 13579],
    [2, 4, 8, 16, 32],
    [2, 3, 5, 7, 11],
    [135, 137, 445],
    [69, 161, 162],
]

def is_private_ip(ip):
    """Check if an IP address is private."""
    return ipaddress.ip_address(ip).is_private

def send_knock_sequence(target_ip, sequence, is_private):
    """Send a knock sequence based on IP type."""
    protocol = "internal" if is_private else "external"
    print(f"Sending knock sequence to {protocol} IP: {sequence}")
    for port in sequence:
        pkt = (
            (IP(dst=target_ip) / TCP(dport=port, flags="S"))
            if is_private
            else (Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst=target_ip) / TCP(dport=port, flags="S"))
        )
        send(pkt, verbose=False)
        time.sleep(0.2)
    print(f"Knock sequence {sequence} sent to {protocol} IP.")

def is_port_open(target_ip, port):
    """Check if a port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            return sock.connect_ex((target_ip, port)) == 0
    except Exception as e:
        print(f"Error checking port {port}: {e}")
        return False

def main(target_ip, target_port):
    """Run the port-knocking process."""
    try:
        is_private = is_private_ip(target_ip)
        print(f"Target IP {target_ip} is {'private' if is_private else 'public'}.")

        for sequence in COMMON_SEQUENCES:
            send_knock_sequence(target_ip, sequence, is_private)
            print("Checking if the target port is open...")
            if is_port_open(target_ip, target_port):
                print(f"SUCCESS: Target port {target_port} is now open after knock sequence: {sequence}")
                break
            else:
                print(f"FAILED: Target port {target_port} is still closed.")
        else:
            print("No successful knock sequences found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Port knocking script with IP and port parameters.")
    parser.add_argument("target_ip", type=str, help="Target IP address to knock on")
    parser.add_argument("target_port", type=int, help="Target port to check after knocking")
    args = parser.parse_args()

    # Run the main function with provided parameters
    main(args.target_ip, args.target_port)
