import socket
import json
import random
import subprocess

def scan_cloudflare_ips():
    domains = [
        "engage.cloudflareclient.com",
        "warp.daemon.cloudflare.com",
        "api.cloudflareclient.com",
        "one.one.one.one",
        "cloudflare.com",
        "www.cloudflare.com",
        "warp.cloudflare.com",
        "warp-relay.cloudflare.com"
    ]
    ipv4_list = []
    ipv6_list = []
    
    for domain in domains:
        try:
            ipv4s = socket.getaddrinfo(domain, None, socket.AF_INET)
            for ip in ipv4s:
                ip_addr = ip[4][0]
                if ip_addr.startswith(("162.159.", "188.114.", "104.", "172.", "182.", "141.", "198.")):
                    if ip_addr not in ipv4_list:
                        ipv4_list.append(ip_addr)
            
            ipv6s = socket.getaddrinfo(domain, None, socket.AF_INET6)
            for ip in ipv6s:
                ip_addr = f"[{ip[4][0]}]"
                if ip_addr.startswith("[2606:4700:") or ip_addr.startswith("[2400:cb00:"):
                    if ip_addr not in ipv6_list:
                        ipv6_list.append(ip_addr)
        except:
            pass
    
    if len(ipv4_list) < 10:
        ipv4_list.extend(["182.161.114." + str(i) for i in range(1, 10)])
        ipv4_list.extend(["162.159.192." + str(i) for i in range(1, 10)])
        ipv4_list.extend(["188.114.96." + str(i) for i in range(1, 10)])
        ipv4_list.extend(["104.16.123." + str(i) for i in range(1, 10)])
    
    if len(ipv6_list) < 10:
        ipv6_list.extend(["[2606:4700:d" + str(i) + "::a29f:c001]" for i in range(0, 10)])
        ipv6_list.extend(["[2400:cb00:a" + str(i) + "::a29f:c001]" for i in range(0, 10)])
    
    random.shuffle(ipv4_list)
    random.shuffle(ipv6_list)
    
    return {"ipv4": ipv4_list[:20], "ipv6": ipv6_list[:20]}

def test_ip(ip, port):
    try:
        if ip.startswith("["):
            ip = ip[1:-1]
            result = subprocess.run(['nc', '-6', '-z', '-w', '2', ip, str(port)], stdout=subprocess.DEVNULL)
        else:
            result = subprocess.run(['nc', '-4', '-z', '-w', '2', ip, str(port)], stdout=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

def filter_working_ips(ips, ports):
    working_ipv4 = []
    working_ipv6 = []
    
    for ip in ips["ipv4"]:
        for port in ports:
            if test_ip(ip, port):
                working_ipv4.append(f"{ip}:{port}")
                break
    
    for ip in ips["ipv6"]:
        for port in ports:
            if test_ip(ip, port):
                working_ipv6.append(f"{ip}:{port}")
                break
    
    if not working_ipv4:
        working_ipv4 = ["162.159.192.1:2408", "162.159.193.1:500"]
    if not working_ipv6:
        working_ipv6 = ["[2606:4700:d0::a29f:c001]:2408", "[2606:4700:d1::a29f:c001]:500"]
    
    return {"ipv4": working_ipv4, "ipv6": working_ipv6}

def save_to_json():
    ips = scan_cloudflare_ips()
    warp_ports = [2408, 500, 1701, 4500, 8080, 8443]
    working_ips = filter_working_ips(ips, warp_ports)
    with open("ips.json", "w") as f:
        json.dump(working_ips, f, indent=4)

if __name__ == "__main__":
    save_to_json()