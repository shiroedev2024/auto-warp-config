import socket
import json
import random

def resolve_cloudflare_ips():
    domains = ["cloudflare.com", "www.cloudflare.com", "one.one.one.one"]
    ipv4_list = []
    ipv6_list = []
    
    for domain in domains:
        try:
            ipv4s = socket.getaddrinfo(domain, None, socket.AF_INET)
            for ip in ipv4s:
                ip_addr = ip[4][0]
                if ip_addr not in ipv4_list:
                    ipv4_list.append(ip_addr)
                    
            ipv6s = socket.getaddrinfo(domain, None, socket.AF_INET6)
            for ip in ipv6s:
                ip_addr = f"[{ip[4][0]}]"
                if ip_addr not in ipv6_list:
                    ipv6_list.append(ip_addr)
        except:
            pass
    
    return {"ipv4": ipv4_list, "ipv6": ipv6_list}

def save_to_json():
    ips = resolve_cloudflare_ips()
    with open("ips.json", "w") as f:
        json.dump(ips, f)

if __name__ == "__main__":
    save_to_json()
