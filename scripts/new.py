import os
import json
import uuid
import shutil
import random
from pathlib import Path
import yaml


def create_directory_structure(node_type, use_caddy):
    directories = {
        'xray': ['config', 'logs'],
        'caddy': ['web', 'data', 'config']
    }

    for main_dir, sub_dirs in directories.items():
        if main_dir == 'caddy' and not use_caddy:
            continue
        for sub_dir in sub_dirs:
            dir_path = f"./{main_dir}/{sub_dir}"
            os.makedirs(dir_path, exist_ok=True)


def generate_xray_config(node_type, node_uuid, upstream_ip=None, upstream_uuid=None):
    shadowsocks_password = 'ir@n3$567123@#'

    config = {}
    if node_type == 'upstream':
        config = {
            "log": {
                "access": "/var/log/xray/access.log",
                "error": "/var/log/xray/error.log",
                "loglevel": "warning"
            },
            "inbounds": [
                {
                    "listen": "0.0.0.0",
                    "port": 1310,
                    "protocol": "vless",
                    "settings": {
                        "clients": [
                            {
                                "id": "",
                                "level": 0
                            }
                        ],
                        "decryption": "none"
                    },
                    "streamSettings": {
                        "network": "ws",
                        "wsSettings": {
                            "path": "/ws"
                        }
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "freedom",
                    "tag": "freedom"
                }
            ],
            "dns": {
                "servers": [
                    "8.8.8.8",
                    "8.8.4.4",
                    "localhost"
                ]
            }
        }
    elif node_type == 'bridge':
        config = {
            "log": {
                "access": "/var/log/xray/access.log",
                "error": "/var/log/xray/error.log",
                "loglevel": "warning"
            },
            "inbounds": [
                {
                    "listen": "0.0.0.0",
                    "port": 1010,
                    "protocol": "socks",
                    "settings": {
                        "auth": "noauth",
                        "udp": True
                    }
                },
                {
                    "listen": "0.0.0.0",
                    "port": 1110,
                    "protocol": "http",
                    "settings": {}
                },
                {
                    "listen": "0.0.0.0",
                    "port": 1210,
                    "protocol": "shadowsocks",
                    "settings": {
                        "password": shadowsocks_password,
                        "method": "aes-128-gcm",
                        "level": 0,
                        "network": "tcp,udp"
                    }
                },
                {
                    "listen": "0.0.0.0",
                    "port": 1310,
                    "protocol": "vless",
                    "settings": {
                        "clients": [
                            {
                                "id": "",
                                "level": 0
                            }
                        ],
                        "decryption": "none"
                    }
                }
            ],
            "outbounds": [
                {
                    "tag": "proxy",
                    "protocol": "vless",
                    "settings": {
                        "vnext": [
                            {
                                "address": "",
                                "port": 1310,
                                "users": [
                                    {
                                        "id": "",
                                        "level": 0
                                    }
                                ]
                            }
                        ]
                    },
                    "streamSettings": {
                        "network": "ws"
                    }
                },
                {
                    "protocol": "freedom",
                    "tag": "freedom"
                }
            ],
            "dns": {
                "servers": [
                    "8.8.8.8",
                    "8.8.4.4",
                    "localhost"
                ]
            },
            "routing": {
                "domainStrategy": "IPIfNonMatch",
                "settings": {
                    "rules": [
                        {
                            "type": "field",
                            "outboundTag": "freedom",
                            "domain": [
                                "regexp:.*\\.ir$"
                            ]
                        }
                    ]
                }
            }
        }

    if node_type == 'upstream':
        config["inbounds"][0]["settings"]["clients"][0]["id"] = node_uuid
    elif node_type == 'bridge':
        config["inbounds"][3]["settings"]["clients"][0]["id"] = node_uuid
        config["outbounds"][0]["settings"]["vnext"][0]["address"] = upstream_ip
        config["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = upstream_uuid

    return config

# ... (rest of the functions remain the same)


# def generate_v2ray_config(node_type, node_uuid, upstream_ip=None, upstream_uuid=None):
#     config = {}
#     if node_type == 'upstream':
#         config = {
#             "log": {
#                 "access": "/var/log/v2ray/access.log",
#                 "error": "/var/log/v2ray/error.log",
#                 "loglevel": "warning"
#             },
#             "inbounds": [
#                 {
#                     "listen": "0.0.0.0",
#                     "port": 1310,
#                     "protocol": "vmess",
#                     "settings": {
#                         "clients": [
#                             {
#                                 "id": "",
#                                 "alterId": 0,
#                                 "security": "auto"
#                             }
#                         ]
#                     },
#                     "streamSettings": {
#                         "network": "ws",
#                         "wsSettings": {
#                             "path": "/ws"
#                         }
#                     },
#                     "mux": {
#                         "enabled": true
#                     }
#                 }
#             ],
#             "outbounds": [
#                 {
#                     "protocol": "freedom",
#                     "tag": "freedom"
#                 }
#             ],
#             "dns": {
#                 "servers": [
#                     "8.8.8.8",
#                     "8.8.4.4",
#                     "localhost"
#                 ]
#             }
#         }
#     elif node_type == 'bridge':
#         config = {
#             "log": {
#                 "access": "/var/log/v2ray/access.log",
#                 "error": "/var/log/v2ray/error.log",
#                 "loglevel": "warning"
#             },
#             "inbounds": [
#                 {
#                     "listen": "0.0.0.0",
#                     "port": 1010,
#                     "protocol": "socks",
#                     "settings": {
#                         "auth": "noauth",
#                         "udp": True
#                     }
#                 },
#                 {
#                     "listen": "0.0.0.0",
#                     "port": 1110,
#                     "protocol": "http",
#                     "settings": {}
#                 },
#                 {
#                     "listen": "0.0.0.0",
#                     "port": 1210,
#                     "protocol": "shadowsocks",
#                     "settings": {
#                         "password": "1234",
#                         "method": "aes-128-gcm",
#                         "level": 0,
#                         "network": "tcp,udp"
#                     }
#                 },
#                 {
#                     "listen": "0.0.0.0",
#                     "port": 1310,
#                     "protocol": "vmess",
#                     "settings": {
#                         "clients": [
#                             {
#                                 "id": "",
#                                 "alterId": 0,
#                                 "security": "aes-128-gcm"
#                             }
#                         ]
#                     }
#                 }
#             ],
#             "outbounds": [
#                 {
#                     "tag": "proxy",
#                     "protocol": "vmess",
#                     "settings": {
#                         "vnext": [
#                             {
#                                 "address": "",
#                                 "port": 1310,
#                                 "users": [
#                                     {
#                                         "id": "",
#                                         "alterId": 0,
#                                         "security": "none"
#                                     }
#                                 ]
#                             }
#                         ]
#                     },
#                     "streamSettings": {
#                         "network": "ws"
#                     },
#                     "mux": {
#                         "enabled": true
#                     }
#                 },
#                 {
#                     "protocol": "freedom",
#                     "tag": "freedom"
#                 }
#             ],
#             "dns": {
#                 "servers": [
#                     "8.8.8.8",
#                     "8.8.4.4",
#                     "localhost"
#                 ]
#             },
#             "routing": {
#                 "domainStrategy": "IPIfNonMatch",
#                 "settings": {
#                     "rules": [
#                         {
#                             "type": "field",
#                             "outboundTag": "freedom",
#                             "domain": [
#                                 "regexp:.*\\.ir$"
#                             ]
#                         }
#                     ]
#                 }
#             }
#         }
#
#     if node_type == 'upstream':
#         config["inbounds"][0]["settings"]["clients"][0]["id"] = node_uuid
#     elif node_type == 'bridge':
#         config["inbounds"][3]["settings"]["clients"][0]["id"] = node_uuid
#         config["outbounds"][0]["settings"]["vnext"][0]["address"] = upstream_ip
#         config["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = upstream_uuid
#
#     return config


def create_caddyfile(domain, node_type):
    caddy_config = f"""{domain} {{
  root * /usr/share/caddy

  @websockets {{
    header Connection *Upgrade*
    header Upgrade    websocket
  }}

  reverse_proxy @websockets v2ray:1310/ws

  route {{
    reverse_proxy /ws v2ray:1310
    file_server
  }}

  log {{
    output stdout
  }}
}}
"""

    if node_type in ['bridge', 'upstream']:
        with open(f"./caddy/Caddyfile", "w") as caddyfile:
            caddyfile.write(caddy_config)


# def create_docker_compose_yml(node_type, use_caddy):
    docker_compose = {
        "version": "3.9",
        "services": {
            "v2ray": {
                # "image": f"ghcr.io/getimages/{'v2ray' if v2ray_or_xray == 'v' else 'xray'}:4.41.1",
                "image": f"ghcr.io/getimages/xray:4.41.1",
                "restart": "always",
                "volumes": [
                    "./v2ray/config/:/etc/v2ray/",
                    "./v2ray/logs:/var/log/v2ray/"
                ],
                "ports": [
                    "127.0.0.1:1310:1310",
                    "127.0.0.1:1310:1310/udp"
                ]
            }
        }
    }

    if node_type == 'upstream' and use_caddy:
        docker_compose["services"]["caddy"] = {
            "image": "ghcr.io/getimages/caddy:2.6.2-alpine",
            "restart": "always",
            "ports": [
                "80:80",
                "80:80/udp",
                "443:443",
                "443:443/udp"
            ],
            "volumes": [
                "./caddy/Caddyfile:/etc/caddy/Caddyfile",
                "./caddy/web/:/usr/share/caddy",
                "./caddy/data/:/data/caddy/",
                "./caddy/config/:/config/caddy"
            ]
        }

    with open("docker-compose.yml", "w") as docker_compose_file:
        yaml.dump(docker_compose, docker_compose_file, sort_keys=False)


def create_docker_compose_yml(node_type, use_caddy=False):
    docker_compose = {
        "version": "3.9",
        "services": {
            "xray": {
                "image": "ghcr.io/getimages/xray:latest",
                "restart": "always",
                "volumes": [
                    "./xray/config/:/etc/xray/",
                    "./xray/logs:/var/log/xray/"
                ],
                "ports": [
                    "127.0.0.1:1310:1310",
                    "127.0.0.1:1310:1310/udp"
                ]
            }
        }
    }

    if node_type == 'upstream' or node_type == 'bridge':
        if use_caddy:
            docker_compose["services"]["caddy"] = {
                "image": "ghcr.io/getimages/caddy:2.6.2-alpine",
                "restart": "always",
                "ports": [
                    "80:80",
                    "80:80/udp",
                    "443:443",
                    "443:443/udp"
                ],
                "volumes": [
                    "./caddy/Caddyfile:/etc/caddy/Caddyfile",
                    "./caddy/web/:/usr/share/caddy",
                    "./caddy/data/:/data/caddy/",
                    "./caddy/config/:/config/caddy"
                ]
            }

    with open("docker-compose.yml", "w") as docker_compose_file:
        yaml.dump(docker_compose, docker_compose_file, sort_keys=False)

# def main():
#     node_type=input(
#         "Enter node type (l - local, b - bridge, u - upstream): ").lower()
#     if node_type not in ['l', 'b', 'u']:
#         print("Invalid node type. Exiting.")
#         return

#     if node_type == 'l':
#         node_type='local'
#     elif node_type == 'b':
#         node_type='bridge'
#     elif node_type == 'u':
#         node_type='upstream'

#     use_caddy=False
#     if node_type == 'bridge' or node_type == 'upstream':
#         use_caddy_input=input(
#             "Do you want to use Caddy for this node? (y/n): ").lower()
#         if use_caddy_input == 'y':
#             use_caddy=True

#     v2ray_or_xray=input("Enter 'v' for v2ray or 'x' for xray: ").lower()
#     if v2ray_or_xray not in ['v', 'x']:
#         print("Invalid choice. Exiting.")
#         return

#     uuid_input=input("Enter UUID (leave empty for auto-generated): ")
#     if not uuid_input:
#         node_uuid=str(uuid.uuid4())
#         print(f"Generated UUID: {node_uuid}")
#     else:
#         try:
#             uuid.UUID(uuid_input)
#             node_uuid=uuid_input
#         except ValueError:
#             print("Invalid UUID. Exiting.")
#             return

#     if node_type == 'bridge':
#         use_same_uuid=input(
#             f"Do you want to use the previously created UUID ({node_uuid}) for upstream? (y/n): ").lower()
#         if use_same_uuid == 'y':
#             upstream_uuid=node_uuid
#         else:
#             upstream_uuid=input("Enter the upstream UUID: ")
#             try:
#                 uuid.UUID(upstream_uuid)
#             except ValueError:
#                 print("Invalid upstream UUID. Exiting.")
#                 return

#         upstream_ip=input("Enter the upstream IP address: ")

#     if node_type == 'bridge' or node_type == 'upstream':
#         domain=input(
#             "Enter the domain to access this node (e.g., upstreamnode1.example.com): ")

#         use_caddy=input(
#             "Do you want to use Caddy as a reverse proxy? (y/n): ").lower() == 'y'
#     if use_caddy and (node_type == 'bridge' or node_type == 'upstream'):
#         domain=input(
#             "Enter the domain to access this node (e.g., upstreamnode1.example.com): ")

#     create_directory_structure(node_type, use_caddy)
#     create_docker_compose_yml(node_type, use_caddy)
#     create_caddyfile(domain, node_type)

#     v2ray_config=generate_v2ray_config(node_type, node_uuid, upstream_ip if node_type ==
#                                                                               'bridge' else None,
#                                          upstream_uuid if node_type == 'bridge' else None)
#     with open(f"./v2ray/config/config.json", "w") as config_file:
#         json.dump(v2ray_config, config_file, indent=2)


# if __name__ == "__main__":
#     main()

def main():
    node_type = input(
        "Enter node type (l - local, b - bridge, u - upstream): ").lower()
    if node_type not in ['l', 'b', 'u']:
        print("Invalid node type. Exiting.")
        return

    if node_type == 'l':
        node_type = 'local'
    elif node_type == 'b':
        node_type = 'bridge'
    elif node_type == 'u':
        node_type = 'upstream'

    uuid_input = input("Enter UUID (leave empty for auto-generated): ")
    if not uuid_input:
        node_uuid = str(uuid.uuid4())
        print(f"Generated UUID: {node_uuid}")
    else:
        try:
            uuid.UUID(uuid_input)
            node_uuid = uuid_input
        except ValueError:
            print("Invalid UUID. Exiting.")
            return

    if node_type == 'bridge' or node_type == 'upstream':
        use_caddy = input("Do you want to use Caddy? (y/n): ").lower() == 'y'
        if use_caddy:
            domain = input(
                "Enter the domain to access this node (e.g., upstreamnode1.example.com): ")
        if node_type == 'bridge':
            use_same_uuid = input(
                f"Do you want to use the previously created UUID ({node_uuid}) for upstream? (y/n): ").lower()
            if use_same_uuid == 'y':
                upstream_uuid = node_uuid
            else:
                upstream_uuid = input("Enter the upstream UUID: ")
                try:
                    uuid.UUID(upstream_uuid)
                except ValueError:
                    print("Invalid upstream UUID. Exiting.")
                    return

            upstream_ip = input("Enter the upstream IP address: ")

    create_directory_structure(node_type, use_caddy)
    create_docker_compose_yml(node_type, use_caddy)

    xray_config = generate_xray_config(node_type, node_uuid, upstream_ip if node_type ==
                                       'bridge' else None, upstream_uuid if node_type == 'bridge' else None)
    with open(f"./xray/config/config.json", "w") as f:
        json.dump(xray_config, f, indent=2)

    if use_caddy:
        create_caddyfile(domain)

    print("Configuration files have been created.")
    print("Run 'docker-compose up -d' to start the containers.")


if __name__ == "__main__":
    main()
