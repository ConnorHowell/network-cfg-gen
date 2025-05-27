# Network Configuration Generator

This script is a simple tool designed to quickly generate multiple network configuration files based on a single base configuration file. The script was made with network switches in mind but is applicable to any network device. It replaces placeholders in the base file with specific values for each switch, such as asset tags, switch numbers, and IP addresses.

## How It Works

1. The script reads a base configuration file (`base.json`).
2. It iterates through a list of asset tags, generating a configuration for each switch.
3. Placeholders in the base file are replaced with specific values:
   - `{ASSET_TAG}`: The asset tag of the switch.
   - `{SW_NUM}`: The switch number (formatted with leading zeros).
   - `{IP_ADDRESS}`: The assigned IP address for the switch.
4. The script checks if the generated IP address is free by pinging it.
5. The generated configurations are saved as individual JSON files.

## Usage

1. Place the script and the `base.json` file in the same directory.
2. Edit the configuration section at the top of the script to customize:
   - `base_file_name`: Name of the base configuration file.
   - `starting_index`: Starting index for switch numbering.
   - `starting_ip_address`: Starting IP address for the switches.
   - `subnet_mask`: Subnet mask (e.g., 24 for a `/24` subnet).
   - `asset_tags`: List of asset tags for the switches.
3. Run the script:
   ```bash
   python build_configs.py
   ```
4. The generated configuration files will be saved in the same directory.

## Placeholders in the Base File
The following placeholders can be used in the base.json file:
- `{ASSET_TAG}`: Replaced with the asset tag of the switch.
- `{SW_NUM}`: Replaced with the switch number (e.g., `01`, `02`).
- `{IP_ADDRESS}`: Replaced with the assigned IP address for the switch.

## Example Base File
```json
{
    "System": {
        "hostname": "SW-{ASSET_TAG}",
        "ntp_config": {
            "enable": "true"
        },
        "other_config": {
            "system_description": "{ASSET_TAG} - Access Switch #{SW_NUM}",
            "system_location": "Server Room"
        }
    },
    "Interface": {
        "vlan80": {
            "ip4_address": "{IP_ADDRESS}/24"
        }
    }
}
```

## TODO:
- Add additional placeholders with modifiers e.g. `IP_ADDRESS.CIDR` for the IP address in CIDR notation
- Add support for IPv6 address generation.
- Allow the script to read asset tags and other parameters from a CSV or JSON file.
- Implement a dry-run mode to preview the generated configurations without writing files.
- Add error handling for missing or malformed base files.
- Improve IP address validation to handle edge cases more robustly.
- Allow customization of the output directory for generated files.
