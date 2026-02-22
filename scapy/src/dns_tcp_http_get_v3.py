from scapy.all import *
from collections import defaultdict
import threading
import time

# Target details
domain = "example.com"
dns_server = "8.8.8.8"
target_port = 80

# DNS resolution
dns_query = IP(dst=dns_server)/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
dns_response = sr1(dns_query, timeout=2, verbose=0)

if not dns_response or dns_response[DNS].ancount == 0:
    print("[-] DNS resolution failed")
    exit()

ip_address = dns_response[DNS].an[0].rdata
print(f"[+] {domain} resolved to {ip_address}")

# TCP handshake
sport = RandShort()
seq = 1000
ip = IP(dst=ip_address)
syn = ip/TCP(sport=sport, dport=target_port, flags='S', seq=seq)
syn_ack = sr1(syn, timeout=2, verbose=0)

if not syn_ack or syn_ack[TCP].flags != 'SA':
    print("[-] No SYN-ACK received")
    exit()

ack = ip/TCP(sport=sport, dport=target_port, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
send(ack, verbose=0)
print("[+] TCP handshake complete")

# HTTP GET request
http_get = f"GET / HTTP/1.1\r\nHost: {domain}\r\nUser-Agent: ScapyClient\r\nConnection: close\r\n\r\n"
payload = Raw(load=http_get)
request = ip/TCP(sport=sport, dport=target_port, flags='PA', seq=syn_ack.ack, ack=syn_ack.seq + 1)/payload

# Shared variable for sniffed packets
captured_packets = []

# Sniffer function (runs in background)
def sniff_response():
    print("[*] Sniffing response...")
    pkts = sniff(
        filter=f"tcp and src host {ip_address} and src port {target_port} and dst port {sport}",
        timeout=5
    )
    captured_packets.extend(pkts)

# Start sniffing in a thread
sniff_thread = threading.Thread(target=sniff_response)
sniff_thread.start()

# Small sleep to ensure sniff has started before send
time.sleep(0.5)

# Send HTTP GET
send(request, verbose=0)
print("[+] HTTP GET request sent")

# Wait for sniffer to finish
sniff_thread.join()

print(f"[+] Sniffed {len(captured_packets)} packets")

# Reassemble payloads
payloads = defaultdict(bytes)

for pkt in captured_packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        payloads[pkt[TCP].seq] = pkt[Raw].load

assembled = b"".join(payloads[k] for k in sorted(payloads))

print("\n--- FULL HTTP RESPONSE ---\n")
print(assembled.decode("utf-8", errors="replace"))
