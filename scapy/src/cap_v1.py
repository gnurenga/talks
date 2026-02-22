import requests
from scapy.all import sniff, wrpcap
import threading

# Function to send the HTTPS request
def send_request():
    response = requests.get("https://icanhazip.com/")
    print("Response:", response.text)

# Function to capture packets
def capture_packets():
    print("Starting packet capture...")
    packets = sniff(timeout=10)  # Capture for 10 seconds
    wrpcap("captured_packets_new.pcap", packets)  # Save captured packets to PCAP file
    print(f"Captured {len(packets)} packets.")

# Create threads for capturing packets and sending request
capture_thread = threading.Thread(target=capture_packets)
capture_thread.start()

# Send the request while capturing packets
send_request()

# Wait for the capture thread to finish
capture_thread.join()

def read_packets(pcap, src, dst):
    pass
    
