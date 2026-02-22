from scapy.all import *

# Target domain and port
domain = "example.com"
dns_server = "8.8.8.8"
target_port = 80

# --- Step 1: DNS Query ---
dns_query = IP(dst=dns_server)/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname=domain, qtype="A"))
dns_response = sr1(dns_query, verbose=0, timeout=2)

if dns_response and dns_response.haslayer(DNS) and dns_response[DNS].ancount > 0:
    ip_address = dns_response[DNS].an[0].rdata
    print(f"[+] {domain} resolved to {ip_address}")
else:
    print("[-] DNS query failed or no answer")
    exit()

# --- Step 2: TCP Handshake ---
sport = RandShort()
seq = 1000

ip = IP(dst=ip_address)
syn = ip/TCP(sport=sport, dport=target_port, flags='S', seq=seq)
syn_ack = sr1(syn, timeout=2, verbose=0)

if not syn_ack or syn_ack[TCP].flags != 'SA':
    print("[-] No SYN-ACK received, cannot establish TCP session")
    exit()

ack = ip/TCP(sport=sport, dport=target_port, flags='A',
             seq=syn_ack.ack, ack=syn_ack.seq + 1)
send(ack, verbose=0)
print("[+] TCP 3-way handshake completed")

# --- Step 3: Send HTTP GET Request ---
http_get = f"GET / HTTP/1.1\r\nHost: {domain}\r\nUser-Agent: ScapyClient\r\nConnection: close\r\n\r\n"
payload = Raw(load=http_get)

request = ip/TCP(sport=sport, dport=target_port, flags='PA',
                 seq=syn_ack.ack, ack=syn_ack.seq + 1)/payload
send(request, verbose=0)
print("[+] HTTP GET request sent")

# --- Step 4: Receive Response ---
# Sniff response packets from the target IP and port
def filter_resp(pkt):
    return pkt.haslayer(TCP) and pkt[IP].src == ip_address and pkt[TCP].sport == target_port and pkt[TCP].dport == sport

print("[*] Waiting for response...")
responses = sniff(filter=filter_resp, timeout=3, count=10)

# Print the response payloads
for pkt in responses:
    if pkt.haslayer(Raw):
        print(pkt[Raw].load.decode(errors="ignore"))
