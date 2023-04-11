# Anti-Censorship V2Ray/Xray Deployment

This project helps set up V2Ray/Xray nodes with Caddy reverse proxy to bypass censorship and DPI filtering in restricted regions.

## Project Structure

├── ansible
│ ├── inventory.ini
│ └── ...
├── config
│ ├── base_xray_config.json
│ ├── localnode1
│ │ ├── caddy
│ │ │ └── Caddyfile
│ │ └── docker
│ │ └── config.json
│ ├── extnode1
│ │ ├── caddy
│ │ │ └── Caddyfile
│ │ └── docker
│ │ └── config.json
│ └── ...
└── update_config.py

- `ansible/`: Contains Ansible inventory and playbooks for deploying the configuration files to the respective servers.
- `config/`: Contains subfolders for each V2Ray/Xray node with their respective Caddy and V2Ray/Xray configuration files.
- `update_config.py`: Python script to update the configuration files based on user input.

## Usage

### Step 1: Clone the repository

Clone this repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>

Step 2: Update the configuration files
Run the update_config.py Python script to create or update the configuration files for a V2Ray/Xray node:

bash
Copy code
python update_config.py
Follow the prompts to provide the necessary information.

Step 3: Deploy the configuration using Ansible
Ensure you have Ansible installed on your local machine. Update the inventory.ini file in the ansible/ folder with the server names and IP addresses. Run the Ansible playbooks to deploy the configuration files to the respective servers:

bash
Copy code
ansible-playbook <playbook_name.yml> -i ansible/inventory.ini
Step 4: Set up the Docker containers
SSH into each server and navigate to the directory containing the configuration files. Use Docker Compose or Docker Swarm to set up the containers on each server:

bash
Copy code
docker-compose up -d
```
