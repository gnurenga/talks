import os
import http.client
import ssl
import threading
from scapy.all import sniff, conf, load_layer

# Set up the environment variable for SSL key logging
os.environ["SSLKEYLOGFILE"] = "secrets.log"

# Function to send an HTTPS request
def send_https_request():
    conn = http.client.HTTPSConnection("icanhazip.com", context=ssl._create_unverified_context())
    conn.request("GET", "/")
    response = conn.getresponse()
    print("Response:", response.read().decode())

# Function to capture packets
def capture_packets():
    print("Starting packet capture...")
    load_layer("tls")
    conf.tls_session_enable = True
    conf.tls_nss_filename = "secrets.log"

    # Sniff packets on port 443 (HTTPS)
    packets = sniff(filter="tcp port 443", timeout=10)

    # Process captured packets
    for packet in packets:
        if packet.haslayer('TLS'):
            print(packet.summary())
            if packet['TLS'].type == 23:  # Application Data type in TLS
                print(packet['TLS'].show())  # Show detailed information about application data

# Start capturing packets in a separate thread
capture_thread = threading.Thread(target=capture_packets)
capture_thread.start()

# Send the HTTPS request while capturing packets
send_https_request()

# Wait for the capture thread to finish
capture_thread.join()
