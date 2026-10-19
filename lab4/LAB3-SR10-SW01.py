from netmiko import ConnectHandler

# ============================================================
# DEVICE INFORMATION
# ============================================================

device = {
    "device_type": "cisco_ios",
    "host": "172.8.4",  # Management IP van SW1
    "username": "student",
    "password": "pxl",
}


# ============================================================
# VLAN INFORMATION
# ============================================================

vlans = {
    118: "Management",
    218: "VM-Hosts",
    318: "Appliance-Servers",
    418: "Data-Users",
    99: "Native",
}


# ============================================================
# CONNECT
# ============================================================

connection = ConnectHandler(**device)

print("Connected to:", connection.find_prompt())


# ============================================================
# CONFIGURATION
# ============================================================

commands = []

# Hostname
commands.append("hostname LAB-SR10-SW01")


# ------------------------------------------------------------
# VLANs aanmaken
# ------------------------------------------------------------

for vlan, name in vlans.items():
    commands.extend([
        f"vlan {vlan}",
        f"name {name}",
        "exit",
    ])


# ------------------------------------------------------------
# Access ports configureren
# ------------------------------------------------------------

# Poorten 1-5: VLAN 210
commands.extend([
    "interface range GigabitEthernet0/1-5",
    "switchport mode access",
    "switchport access vlan 218",
    "no shutdown",
    "exit",
])

# Poorten 6-10: VLAN 310
commands.extend([
    "interface range GigabitEthernet0/6-10",
    "switchport mode access",
    "switchport access vlan 318",
    "no shutdown",
    "exit",
])

# Poorten 11-20: VLAN 410
commands.extend([
    "interface range GigabitEthernet0/11-20",
    "switchport mode access",
    "switchport access vlan 418",
    "no shutdown",
    "exit",
])

# Poorten 21-22: VLAN 110
commands.extend([
    "interface range GigabitEthernet0/21-22",
    "switchport mode access",
    "switchport access vlan 118",
    "no shutdown",
    "exit",
])


# ------------------------------------------------------------
# Trunk naar de router
# ------------------------------------------------------------

commands.extend([
    "interface range GigabitEthernet0/23-24",
    "switchport mode trunk",
    "switchport trunk allowed vlan 118,218,318,418,99",
    "switchport trunk native vlan 99",
    "no shutdown",
    "exit",
])


# ============================================================
# SEND CONFIGURATION
# ============================================================

print("\nConfiguring SW1...\n")

output = connection.send_config_set(commands)

print(output)


# ============================================================
# VERIFICATION
# ============================================================

print("\n========================================")
print("VLAN STATUS")
print("========================================")

print(connection.send_command("show vlan brief"))


print("\n========================================")
print("TRUNK STATUS")
print("========================================")

print(connection.send_command("show interfaces trunk"))


print("\n========================================")
print("INTERFACE STATUS")
print("========================================")

print(connection.send_command("show ip interface brief"))


print("\n========================================")
print("RUNNING CONFIGURATION")
print("========================================")

print(connection.send_command("show running-config"))


# ============================================================
# DISCONNECT
# ============================================================

connection.disconnect()

print("\nDisconnected.")