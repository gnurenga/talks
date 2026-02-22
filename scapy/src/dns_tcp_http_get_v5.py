import socket
import os
import time
from scapy.all import *

# ------------------------------
# Parameters
# ------------------------------
domain = "example.com"
dport = 80
sport = RandShort()

# ------------------------------
# Resolve domain to IP
# ------------------------------
dst_ip = socket.gethostbyname(domain)
print(f"[+] {domain} resolved to {dst_ip}")

# ------------------------------
# Drop RSTs from Linux kernel
# ------------------------------
os.system(f"sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -d {dst_ip} --dport {dport} -j DROP")

# ------------------------------
# TCP Handshake
# ------------------------------
ip = IP(dst=dst_ip)
syn = TCP(sport=sport, dport=dport, flags="S", seq=1000)
synack = sr1(ip/syn, timeout=2, verbose=0)

if not synack:
    print("[-] No SYN-ACK received")
    exit()

ack = TCP(sport=sport, dport=dport, flags="A", seq=synack.ack, ack=synack.seq + 1)
send(ip/ack, verbose=0)
print("[+] TCP handshake complete")

# ------------------------------
# Send HTTP GET request
# ------------------------------
http_get = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
get_pkt = TCP(sport=sport, dport=dport, flags="PA", seq=synack.ack, ack=synack.seq + 1)
send(ip/get_pkt/http_get, verbose=0)
print("[+] HTTP GET sent")

# ------------------------------
# HTTP Response Collector
# ------------------------------
response_data = []
current_seq = None

def handle_packet(pkt):
    global current_seq

    if pkt.haslayer(TCP) and pkt[TCP].sport == dport and pkt[IP].src == dst_ip:
        payload = bytes(pkt[TCP].payload)
        if payload:
            response_data.append(payload)

            # Send ACK back to server
            ack_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
                      TCP(sport=pkt[TCP].dport,
                          dport=pkt[TCP].sport,
                          seq=pkt[TCP].ack,
                          ack=pkt[TCP].seq + len(payload),
                          flags="A")
            send(ack_pkt, verbose=0)

# ------------------------------
# Sniffing in parallel
# ------------------------------
print("[*] Sniffing response...")
sniffer = AsyncSniffer(filter=f"tcp and src host {dst_ip} and src port {dport}", prn=handle_packet)
sniffer.start()
time.sleep(5)
sniffer.stop()

# ------------------------------
# Output the HTTP Response
# ------------------------------
print("\n--- FULL HTTP RESPONSE ---")
http_response = b''.join(response_data)
print(http_response.decode(errors="ignore"))

# ------------------------------
# Clean up iptables rule
# ------------------------------
os.system(f"sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST -d {dst_ip} --dport {dport} -j DROP")
