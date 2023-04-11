import json
import os
import uuid

def get_server_info():
    server_type = input("Enter the server type (local or external): ")
    server_name = input("Enter the server name (e.g., localnode1, extnode1): ")
    ip_address = input(f"Enter the IP address for {server_name}: ")
    dns = input(f"Enter the DNS name for {server_name}: ")

    return {
        'server_type': server_type,
        'server_name': server_name,
        'ip': ip_address,
        'dns': dns,
    }

def create_folders(server_name):
    os.makedirs(f'config/{server_name}/docker', exist_ok=True)
    os.makedirs(f'config/{server_name}/caddy', exist_ok=True)

def create_caddyfile(server_name, server_info):
    caddyfile_content = f"""https://{server_info['dns']} {{
    reverse_proxy * 127.0.0.1:10000
}}
"""

    with open(f'config/{server_name}/caddy/Caddyfile', 'w') as f:
        f.write(caddyfile_content)

def create_xray_config(server_name, server_info):
    with open('config/base_xray_config.json', 'r') as f:
        xray_config = json.load(f)

    for inbound in xray_config['inbounds']:
        if 'settings' in inbound and 'clients' in inbound['settings']:
            for client in inbound['settings']['clients']:
                client['id'] = str(uuid.uuid4())

    with open(f'config/{server_name}/docker/config.json', 'w') as f:
        json.dump(xray_config, f, indent=2)

def update_ansible_inventory(ansible_inventory_file, server_info, server_group):
    with open(ansible_inventory_file, 'r') as f:
        inventory_content = f.readlines()

    updated_content = []
    server_entry = f"{server_info['server_name']} ansible_host={server_info['ip']}\n"
    found_group = False

    for line in inventory_content:
        if line.strip() == f"[{server_group}]":
            found_group = True
        elif found_group and server_info['server_name'] in line:
            line = server_entry
            found_group = False

        updated_content.append(line)

    with open(ansible_inventory_file, 'w') as f:
        f.writelines(updated_content)

server_info = get_server_info()

server_group = "local_nodes" if server_info['server_type'] == "local" else "external_nodes"
ansible_inventory_file = "ansible/inventory.ini"

create_folders(server_info['server_name'])
create_caddyfile(server_info['server_name'], server_info)
create_xray_config(server_info['server_name'], server_info)
update_ansible_inventory(ansible_inventory_file, server_info, server_group)
