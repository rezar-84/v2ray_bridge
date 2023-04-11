import json
import uuid
from pathlib import Path
import subprocess


def prompt_user():
    node_type = input("Enter node type (localnode/extnode): ")
    node_number = int(input("Enter node number: "))
    hostname = input("Enter hostname: ")
    ip_address = input("Enter IP address: ")
    domain = input("Enter domain: ")
    user_uuid = input("Enter UUID (leave empty to generate a new one): ")
    if not user_uuid:
        user_uuid = str(uuid.uuid4())
        print(f"Generated UUID: {user_uuid}")
    return node_type, node_number, hostname, ip_address, domain, user_uuid


def create_node_dirs(node_type, node_number):
    node_name = f"{node_type}{node_number}"
    base_path = Path("config") / node_name
    caddy_path = base_path / "caddy"
    docker_path = base_path / "docker"

    base_path.mkdir(parents=True, exist_ok=True)
    caddy_path.mkdir(parents=True, exist_ok=True)
    docker_path.mkdir(parents=True, exist_ok=True)

    return node_name, base_path, caddy_path, docker_path


def create_caddyfile(caddy_path, hostname, domain):
    caddyfile_path = caddy_path / "Caddyfile"
    if not caddyfile_path.exists():
        with caddyfile_path.open("w") as f:
            f.write(f"{domain} {{\n")
            f.write("  reverse_proxy localhost:10000\n")
            f.write("  encode zstd gzip\n")
            f.write("  tls internal\n")
            f.write("}\n")


def create_docker_config(docker_path, node_type, hostname, ip_address, domain, user_uuid):
    config_path = docker_path / "config.json"
    if not config_path.exists():
        (Path("config") / "base_xray_config.json").copy(config_path)

        with config_path.open("r") as f:
            config = json.load(f)

        config["inbounds"][0]["settings"]["clients"][0]["id"] = user_uuid
        config["inbounds"][0]["settings"]["clients"][0]["email"] = f"{hostname}@{domain}"
        config["inbounds"][0]["streamSettings"]["wsSettings"]["headers"]["Host"] = domain
        config["inbounds"][0]["streamSettings"]["xtlsSettings"]["servername"] = domain

        if node_type == "localnode":
            config["routing"]["rules"][0]["outboundTag"] = "direct"
        else:
            config["routing"]["rules"][0]["outboundTag"] = "proxy"
            config["outbounds"][0]["settings"]["vnext"][0]["address"] = ip_address

        with config_path.open("w") as f:
            json.dump(config, f, indent=2)


def install_bbr():
    install = input("Do you want to install BBR? (y/n): ")
    if install.lower() == 'y':
        subprocess.run(["wget", "--no-check-certificate",
                       "https://github.com/teddysun/across/raw/master/bbr.sh"])
        subprocess.run(["chmod", "+x", "bbr.sh"])
        subprocess.run(["./bbr.sh"], check=True)


def main():
    while True:
        node_type, node_number, hostname, ip_address, domain, user_uuid = prompt_user()
        node_name, base_path, caddy_path, docker_path = create_node_dirs(
            node_type, node_number)
        create_caddyfile(caddy_path, hostname, domain)
        create_docker_config(docker_path, node_type,
                             hostname, ip_address, domain, user_uuid)
        install_bbr()

        create_another = input("Do you want to create another node? (y/n): ")
        if create_another.lower() != 'y':
            break


if __name__ == "__main__":
    main()
