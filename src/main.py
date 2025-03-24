import json
import random
import requests
import os
from datetime import datetime

def fetch_ips():
    try:
        response = requests.get('https://raw.githubusercontent.com/Dream68/Warp-IP-Scanner/main/warp_ip.json')
        data = response.json()
        return data
    except Exception as e:
        return {
            "ipv4": ["162.159.193.10:2408", "162.159.195.87:8888"],
            "ipv6": ["[2606:4700:d0::a29f:c057]:8080"]
        }

def generate_config(ip_port, index, ip_version):
    base = f"warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4&&detour=warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4#Anon-WoW-{ip_version}🇩🇪-{index}"
    return base

def update_config_file():
    with open('src/templates/config_template.txt', 'r', encoding='utf-8') as f:
        template = f.read()

    ips = fetch_ips()
    
    ipv4 = random.choice(ips['ipv4'])
    ipv6 = random.choice(ips['ipv6'])
    
    configs = []
    configs.append("warp://auto")
    configs.append(generate_config(ipv4, 2, "IPv4"))
    configs.append(generate_config(ipv6, 3, "IPv6"))
    
    final_config = template + "\n" + "\n\n".join(configs)
    
    with open('config.txt', 'w', encoding='utf-8') as f:
        f.write(final_config)

if __name__ == "__main__":
    update_config_file()