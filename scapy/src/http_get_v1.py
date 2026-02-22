from scapy.all import *

# Target details
dst_ip = "93.184.216.34"  # example.com
dst_port = 80
src_port = RandShort()

# 1. SYN
ip = IP(dst=dst_ip)
syn = TCP(sport=src_port, dport=dst_port, flags="S", seq=1000)
syn_ack = sr1(ip/syn, timeout=2)

# 2. SYN-ACK received, send ACK
ack = TCP(sport=src_port, dport=dst_port, flags="A", 
          seq=syn_ack.ack, ack=syn_ack.seq + 1)

send(ip/ack)

# 3. Send HTTP GET request
http_payload = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "User-Agent: Scapy\r\n"
    "Accept: */*\r\n"
    "Connection: close\r\n\r\n"
)

psh = TCP(sport=src_port, dport=dst_port, flags="PA",
          seq=ack.seq, ack=ack.ack)
send(ip/psh/http_payload)

# 4. Receive HTTP response
def receive_response(pkt):
    if pkt.haslayer(Raw):
        print(pkt[Raw].load.decode(errors="ignore"))

sniff(filter=f"tcp and src host {dst_ip} and port {dst_port}", 
      prn=receive_response, timeout=5)
