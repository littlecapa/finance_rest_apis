from fastapi import FastAPI
import netifaces as ni

app = FastAPI()

# Function to get the IP address of the container
def get_ip_address():
    interfaces = ni.interfaces()
    ip_address = "Not Found"
    for interface in interfaces:
        if interface == 'lo':  # skip loopback interface
            continue
        addresses = ni.ifaddresses(interface)
        if ni.AF_INET in addresses:
            ip_address = addresses[ni.AF_INET][0]['addr']
            break
    return ip_address