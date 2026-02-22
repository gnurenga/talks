from scapy.all import *
from collections import defaultdict

# --- Step 1: DNS Resolution ---
domain = "example.com"
dns_server = "8.8.8.8"
target_port = 80

dns_query = IP(dst=dns_server)/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname=domain, qtype="A"))
dns_response = sr1(dns_query, verbose=0, timeout=2)

if not dns_response or not dns_response.haslayer(DNS) or dns_response[DNS].ancount == 0:
    print("[-] DNS failed")
    exit()

ip_address = dns_response[DNS].an[0].rdata
print(f"[+] {domain} resolved to {ip_address}")

# --- Step 2: TCP Handshake ---
sport = RandShort()
seq = 1000
ip = IP(dst=ip_address)
syn = ip/TCP(sport=sport, dport=target_port, flags='S', seq=seq)
syn_ack = sr1(syn, timeout=2, verbose=0)

if not syn_ack or syn_ack[TCP].flags != 'SA':
    print("[-] SYN-ACK not received")
    exit()

ack = ip/TCP(sport=sport, dport=target_port, flags='A',
             seq=syn_ack.ack, ack=syn_ack.seq + 1)
send(ack, verbose=0)
print("[+] TCP handshake complete")

# --- Step 3: Send HTTP GET ---
http_get = f"GET / HTTP/1.1\r\nHost: {domain}\r\nUser-Agent: ScapyClient\r\nConnection: close\r\n\r\n"
payload = Raw(load=http_get)
request = ip/TCP(sport=sport, dport=target_port, flags='PA',
                 seq=syn_ack.ack, ack=syn_ack.seq + 1)/payload
send(request, verbose=0)
print("[+] HTTP GET request sent")

# --- Step 4: Receive and Reassemble Response ---
# Define filter
bpf_filter = f"tcp and src host {ip_address} and src port {target_port} and dst port {sport}"

# Capture packets
print("[*] Sniffing response...")
packets = sniff(filter=bpf_filter, timeout=10, count = 0)

# Collect payloads keyed by sequence number
payloads = defaultdict(bytes)

for pkt in packets:
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        seq_num = pkt[TCP].seq
        payloads[seq_num] = pkt[Raw].load

# Reassemble in order
print("[*] Reassembling response...")
assembled = b"".join([payloads[k] for k in sorted(payloads)])

# Print the result
try:
    response_text = assembled.decode("utf-8", errors="replace")
    print("\n--- FULL HTTP RESPONSE ---\n")
    print(response_text)
except Exception as e:
    print(f"[-] Failed to decode response: {e}")
