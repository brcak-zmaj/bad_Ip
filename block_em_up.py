import re
import subprocess
import requests

GITHUB_RAW_LINKS = [
    "https://raw.githubusercontent.com/brcak-zmaj/bad_Ip/main/list_01",
    "https://raw.githubusercontent.com/antoinevastel/avastel-bot-ips-lists/master/avastel-ips-7d.txt"
]

# Function to extract IP addresses from a given text
def extract_ips(text):
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ips = re.findall(ip_pattern, text)
    return ips

# Function to add IP addresses to UFW block list
def block_ips(ips):
    for ip in ips:
        # Check if the IP address is already blocked
        result = subprocess.run(["ufw", "status", "numbered"], capture_output=True, text=True)
        if ip in result.stdout:
            continue

        # Block the IP address using UFW
        subprocess.run(["ufw", "deny", "from", ip])
        print(f"Blocked IP: {ip}")

# Monitor GitHub raw links
def monitor_github_links(links):
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                ips = extract_ips(response.text)
                block_ips(ips)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from {link}: {str(e)}")

# Start monitoring GitHub raw links
monitor_github_links(GITHUB_RAW_LINKS)
