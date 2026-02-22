from scapy.all import *
import threading
import time

# --- Configuration ---
domain = "example.com"
dport = 80
sport = RandShort()
iface = None  # or specify like "eth0"

# --- Step 1: DNS Resolution ---
dns_resp = sr1(IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=domain)), verbose=0)
dst_ip = dns_resp[DNS].an.rdata
print(f"[+] {domain} resolved to {dst_ip}")

# --- Step 2: TCP Handshake ---
ip = IP(dst=dst_ip)
syn = TCP(sport=sport, dport=dport, flags="S", seq=1000)
syn_ack = sr1(ip/syn, timeout=2, verbose=0)
if not syn_ack or syn_ack[TCP].flags != "SA":
    print("[-] SYN-ACK failed")
    exit()

ack = TCP(sport=sport, dport=dport, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
send(ip/ack, verbose=0)
print("[+] TCP handshake complete")

# --- Step 3: HTTP GET ---
http_get = f"GET / HTTP/1.1\r\nHost: {domain}\r\nUser-Agent: Scapy\r\nConnection: close\r\n\r\n"
get_pkt = TCP(sport=sport, dport=dport, flags="PA", seq=ack.seq, ack=ack.ack)
send(ip/get_pkt/http_get, verbose=0)
print("[+] HTTP GET sent")

# Track sequence numbers
client_seq = ack.seq + len(http_get)
client_ack = ack.ack
response_data = []

# --- Step 4: Sniff Response & ACK ---
def handle_packet(pkt):
    global client_seq, client_ack
    if pkt.haslayer(TCP) and pkt[IP].src == dst_ip and pkt[TCP].sport == dport:
        payload = bytes(pkt[TCP].payload)
        if payload:
            response_data.append(payload)
            # Send ACK back to server
            ack_pkt = IP(dst=dst_ip, src=pkt[IP].dst)/TCP(
                sport=sport,
                dport=dport,
                seq=client_seq,
                ack=pkt[TCP].seq + len(payload),
                flags="A"
            )
            send(ack_pkt, verbose=1)
            client_ack = pkt[TCP].seq + len(payload)

# --- Step 5: Sniff in Parallel ---
sniffer = AsyncSniffer(filter=f"tcp and src host {dst_ip} and dst port {sport}", prn=handle_packet, iface=iface)
sniffer.start()
time.sleep(5)  # Wait for response to arrive (adjust if needed)
sniffer.stop()

# --- Step 6: Reassemble and Print ---
print("\n--- FULL HTTP RESPONSE ---")
print(b"".join(response_data).decode(errors="ignore"))
