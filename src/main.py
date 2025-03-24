import json
import random

def load_ips():
    try:
        with open("ips.json", "r") as f:
            return json.load(f)
    except:
        return {
            "ipv4": ["1.1.1.1", "1.0.0.1"],
            "ipv6": ["[2606:4700:4700::1111]", "[2606:4700:4700::1001]"]
        }

def generate_config(ip, port, index, ip_version):
    return f"warp://{ip}:{port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4&&detour=warp://{ip}:{port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4#Anon-WoW-{ip_version}🇩🇪-{index}"

def update_config_file():
    with open("src/templates/config_template.txt", "r", encoding="utf-8") as f:
        template = f.read()

    ips = load_ips()
    ipv4 = random.choice(ips["ipv4"])
    ipv6 = random.choice(ips["ipv6"])
    port_ipv4 = random.randint(8000, 9000)
    port_ipv6 = random.randint(8000, 9000)
    
    configs = []
    configs.append("warp://auto")
    configs.append(generate_config(ipv4, port_ipv4, 2, "IPv4"))
    configs.append(generate_config(ipv6, port_ipv6, 3, "IPv6"))
    
    final_config = template + "\n" + "\n\n".join(configs)
    
    with open("config.txt", "w", encoding="utf-8") as f:
        f.write(final_config)

if __name__ == "__main__":
    update_config_file()