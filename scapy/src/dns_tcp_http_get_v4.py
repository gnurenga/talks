from scapy.all import *
from collections import defaultdict
import threading
import time

# Setup
domain = "example.com"
dns_server = "8.8.8.8"
target_port = 80
sport = RandShort()

# --- Step 1: DNS resolution ---
dns_query = IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
dns_response = sr1(dns_query, timeout=2, verbose=0)

if not dns_response or dns_response[DNS].ancount == 0:
    print("[-] DNS resolution failed")
    exit()

ip_address = dns_response[DNS].an[0].rdata
print(f"[+] {domain} resolved to {ip_address}")

# --- Step 2: TCP 3-Way Handshake ---
seq_num = random.randint(0, 2**32 - 1)
ip = IP(dst=ip_address)
syn = ip/TCP(sport=sport, dport=target_port, flags="S", seq=seq_num)
syn_ack = sr1(syn, timeout=2, verbose=0)

if not syn_ack or syn_ack[TCP].flags != "SA":
    print("[-] No SYN-ACK received")
    exit()

ack_num = syn_ack.seq + 1
client_seq = seq_num + 1

ack_pkt = ip/TCP(sport=sport, dport=target_port, flags="A", seq=client_seq, ack=ack_num)
send(ack_pkt, verbose=0)
print("[+] TCP handshake complete")

# --- Step 3: Prepare HTTP GET ---
http_get = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
payload = Raw(load=http_get)

get_pkt = ip/TCP(sport=sport, dport=target_port, flags="PA", seq=client_seq, ack=ack_num)/payload

# --- Step 4: Start Sniffer Thread ---
captured_packets = []

def sniff_response():
    bpf = f"tcp and src host {ip_address} and src port {target_port} and dst port {sport}"
    pkts = sniff(filter=bpf, timeout=5)
    captured_packets.extend(pkts)

sniffer_thread = threading.Thread(target=sniff_response)
sniffer_thread.start()
time.sleep(0.3)  # Allow sniffer to start

# --- Step 5: Send HTTP GET ---
send(get_pkt, verbose=0)
print("[+] HTTP GET sent")

sniffer_thread.join()
print(f"[+] Sniffed {len(captured_packets)} packets")

# --- Step 6: Reassemble and Print Response ---
payloads = defaultdict(bytes)

for pkt in captured_packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        payloads[pkt[TCP].seq] = pkt[Raw].load

assembled = b"".join(payloads[k] for k in sorted(payloads))

print("\n--- FULL HTTP RESPONSE ---\n")
print(assembled.decode("utf-8", errors="replace"))
