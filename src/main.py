import json
import random

def load_ips():
    try:
        with open("ips.json", "r") as f:
            return json.load(f)
    except:
        return {
            "ipv4": ["162.159.192.1", "162.159.193.1"],
            "ipv6": ["[2606:4700:d0::a29f:c001]", "[2606:4700:d1::a29f:c001]"]
        }

def generate_config(ip, port, index, ip_version):
    return f"warp://{ip}:{port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4&&detour=warp://{ip}:{port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4#Anon-WoW-{ip_version}🇩🇪-{index}"

def update_config_file():
    with open("src/templates/config_template.txt", "r", encoding="utf-8") as f:
        template = f.read()

    ips = load_ips()
    ipv4 = random.choice(ips["ipv4"])
    ipv6 = random.choice(ips["ipv6"])
    
    warp_ports = [2408, 500, 1701, 4500, 8080, 8443]
    port_ipv4 = random.choice(warp_ports)
    port_ipv6 = random.choice(warp_ports)
    
    configs = []
    configs.append("warp://auto")
    configs.append(generate_config(ipv4, port_ipv4, 1, "IPv4"))
    configs.append(generate_config(ipv6, port_ipv6, 2, "IPv6"))
    
    final_config = template + "\n" + "\n\n".join(configs)
    
    with open("config.txt", "w", encoding="utf-8") as f:
        f.write(final_config)

if __name__ == "__main__":
    update_config_file()