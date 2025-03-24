import json
import random

def load_ips():
    try:
        with open("ips.json", "r") as f:
            ips = json.load(f)
            if not ips["ipv4"]:
                ips["ipv4"] = ["162.159.192.1:2408", "162.159.193.1:500"]
            if not ips["ipv6"]:
                ips["ipv6"] = ["[2606:4700:d0::a29f:c001]:2408", "[2606:4700:d1::a29f:c001]:500"]
            return ips
    except:
        return {
            "ipv4": ["162.159.192.1:2408", "162.159.193.1:500"],
            "ipv6": ["[2606:4700:d0::a29f:c001]:2408", "[2606:4700:d1::a29f:c001]:500"]
        }

def generate_config(ip_port, index, ip_version):
    return f"warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4&&detour=warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4#Anon-WoW-{ip_version}🇩🇪-{index}"

def update_config_file():
    with open("src/templates/config_template.txt", "r", encoding="utf-8") as f:
        template = f.read()

    ips = load_ips()
    ipv4 = random.choice(ips["ipv4"])
    ipv6 = random.choice(ips["ipv6"])
    
    configs = []
    configs.append("warp://auto")
    configs.append(generate_config(ipv4, 1, "IPv4"))
    configs.append(generate_config(ipv6, 2, "IPv6"))
    
    final_config = template + "\n" + "\n\n".join(configs)
    
    with open("config.txt", "w", encoding="utf-8") as f:
        f.write(final_config)

if __name__ == "__main__":
    update_config_file()