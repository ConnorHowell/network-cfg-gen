import subprocess
import ipaddress

# CONFIGURATION SECTION
# ==================================================
# Edit these variables to customize the configuration generation.

base_file_name = 'base.json'  # Name of the base configuration file
starting_index = 1  # Starting index for switch numbering
starting_ip_address = '192.168.8.1'  # Starting IP address for the switches
subnet_mask = 24  # Subnet mask (e.g., 24 for /24 subnet)
asset_tags = [  # List of asset tags for the switches
    '1012',
    '1013',
    '1014',
    '1015',
    '1016',
    '1017',
    '1018',
]

# DO NOT EDIT BELOW THIS LINE
# ==================================================

# Load the base configuration file
base_file = open(base_file_name, 'r').read()

# Placeholders in the base file:
# - {ASSET_TAG}: Replaced with the asset tag
# - {SW_NUM}: Replaced with the switch number
# - {IP_ADDRESS}: Replaced with the assigned IP address


def is_ip_free(ip_address):
    """
    Check if an IP address is free by pinging it.

    Args:
        ip_address (str): The IP address to check.

    Returns:
        bool: True if the IP address is free, False if it is in use.
    """
    try:
        # Ping the IP address with a timeout of 1 second
        result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip_address],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode != 0  # Return True if the IP is free
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m Error checking IP {ip_address}: {e}")
        return False


def generate_ip(base_ip, offset, subnet_mask):
    """
    Generate a new IP address by adding an offset to the base IP and validate it against the subnet mask.

    Args:
        base_ip (str): The base IP address.
        offset (int): The offset to add to the base IP.
        subnet_mask (int): The subnet mask (e.g., 24 for /24 subnet).

    Returns:
        str: The generated IP address, or None if it is invalid.
    """
    try:
        base = ipaddress.IPv4Address(base_ip)
        new_ip = base + offset
        network = ipaddress.IPv4Network(f"{base_ip}/{subnet_mask}", strict=False)

        # Ensure the new IP is within the subnet and not .0 or .255
        if new_ip not in network or new_ip == network.network_address or new_ip == network.broadcast_address:
            raise ValueError("IP address is invalid (network or broadcast address)")
        return str(new_ip)
    except (ipaddress.AddressValueError, ValueError) as e:
        print(f"\033[91m[ERROR]\033[0m Error generating IP address: {e}")
        return None


# Generate a JSON configuration for each asset tag
configs = []
ip_status = []  # To store the status of each IP address

print("\033[94m✨ Configuration generation script started! ✨\033[0m")
print(f"\033[93m📄 Base file:\033[0m {base_file_name}")
print(f"\033[93m🔢 Starting index:\033[0m {starting_index}")
print(f"\033[93m🌐 Starting IP address:\033[0m {starting_ip_address}")
print(f"\033[93m🛡️ Subnet mask:\033[0m /{subnet_mask}")
print(f"\033[93m📦 Number of asset tags:\033[0m {len(asset_tags)}")
print("\n\033[94m🚀 Processing asset tags step by step:\033[0m\n")

for i, asset_tag in enumerate(asset_tags, start=starting_index):
    print(f"\033[96m➡️ Processing Asset Tag: {asset_tag} (Switch #{i:02})...\033[0m")

    config = base_file.replace('{ASSET_TAG}', asset_tag)
    sw_num = f"{i:02}"  # Format the switch number with leading zeros
    config = config.replace('{SW_NUM}', sw_num)
    ip_address = generate_ip(starting_ip_address, i - 1, subnet_mask)

    if ip_address is None:
        ip_status.append(("Invalid", "Invalid Address"))
        config = config.replace('{IP_ADDRESS}', "Invalid (Invalid Address)")
        print(f"  \033[91m❌ IP Address: Invalid (Invalid Address)\033[0m")
    elif is_ip_free(ip_address):
        config = config.replace('{IP_ADDRESS}', ip_address)
        ip_status.append((ip_address, "Free"))
        print(f"  \033[92m✅ IP Address: {ip_address} (Free)\033[0m")
    else:
        config = config.replace('{IP_ADDRESS}', f"{ip_address} (IN USE)")
        ip_status.append((ip_address, "In Use"))
        print(f"  \033[93m⚠️ IP Address: {ip_address} (In Use)\033[0m")

    configs.append(config)

print("\n\033[94m💾 Writing configurations to files...\033[0m\n")

# Write the configurations to individual files
for i, config in enumerate(configs, start=starting_index):
    file_name = f'{asset_tags[i - starting_index]}.json'
    with open(file_name, 'w') as f:
        f.write(config)
    print(f"  \033[92m✅ Written:\033[0m {file_name}")

print("\n\033[94m📋 Generated configurations overview:\033[0m")
for i, asset_tag in enumerate(asset_tags, start=starting_index):
    sw_num = f"{i:02}"  # Ensure consistent formatting in the output
    ip_address, status = ip_status[i - starting_index]
    print(f"  \033[96m➡️ {asset_tag}.json - Asset Tag: {asset_tag}, Switch #: {sw_num}, IP Address: {ip_address} ({status})\033[0m")

print("\n\033[92m🎉 Configuration generation completed successfully! 🎉\033[0m")
