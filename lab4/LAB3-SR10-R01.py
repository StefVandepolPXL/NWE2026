from netmiko import ConnectHandler

# ============================================================
# DEVICE INFORMATION
# ============================================================

device = {
    "device_type": "cisco_ios",
    "host": "172.16.18.2",       # Management IP van R1
    "username": "student",
    "password": "pxl",
}


# ============================================================
# VLAN INFORMATION
# ============================================================

vlans = {
    118: "172.16.18.2",
    218: "172.16.18.66",
    318: "172.16.18.130",
    418: "172.16.18.194"
}

networks = {
    118: "172.16.18.0",
    218: "172.16.18.64",
    318: "172.16.18.128",
    418: "172.16.18.192"



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
commands.append("hostname LAB-SR18-R01")


# ------------------------------------------------------------
# Router-on-a-stick subinterfaces
# ------------------------------------------------------------

for vlan, ip in vlans.items():

    commands.append(
        f"interface GigabitEthernet0/0/0.{vlan}"
    )

    commands.append(
        f"encapsulation dot1Q {vlan}"
    )

    commands.append(
        f"ip address {ip} 255.255.255.192"
    )

# Subinterface voor Native VLAN

commands.extend([
    "interface GigabitEthernet0/0/0.99",
    "encapsulation dot1Q 99 native",
])

# ------------------------------------------------------------
# Outside interface
# ------------------------------------------------------------

commands.extend([
    "interface GigabitEthernet0/0/1",
    "ip address 10.199.66.210 255.255.255.224",
    "no shutdown",
])


# ------------------------------------------------------------
# OSPF
# ------------------------------------------------------------

commands.extend([
    "router ospf 10",
    "router-id 10.10.10.10",
    "network 172.16.18.0 0.0.0.63 area 0",
    "network 172.16.18.64 0.0.0.63 area 0",
    "network 172.16.18.128 0.0.0.63 area 0",
    "network 172.16.18.192 0.0.0.63 area 0",
    "network 10.199.66.192 0.0.0.31 area 0",

    "default-information originate",
])

# ------------------------------------------------------------
# ACL
# ------------------------------------------------------------

# ACL configureren
commands.append("ip access-list extended OUTSIDE_IN")
commands.append("permit ospf any any")

for vlan, network in networks.items():

    if vlan == 118:
        commands.append(f"deny ip any {network} 0.0.0.63")
    else:
        commands.append(f"permit ip any {network} 0.0.0.63")

commands.append("exit")

commands.append("ip access-list extended INSIDE_OUT")
commands.append("permit ospf any any")

for vlan, network in networks.items():

    if vlan == 118:
        commands.append(f"deny ip {network} 0.0.0.63 any")
    else:
        commands.append(f"permit ip {network} 0.0.0.63 any")

commands.append("exit")

# ACL aan interface koppelen
commands.extend([
    "interface GigabitEthernet0/0/1",
    "ip access-group OUTSIDE_IN in",
    "ip access-group INSIDE_OUT out",
    "exit",
])

# ============================================================
# SEND CONFIGURATION
# ============================================================

print("\nConfiguring R1...\n")

output = connection.send_config_set(commands)

print(output)


# ============================================================
# VERIFICATION
# ============================================================

print("\n========================================")
print("INTERFACE STATUS")
print("========================================")

print(
    connection.send_command("show ip interface brief")
)


print("\n========================================")
print("ROUTING TABLE")
print("========================================")

print(
    connection.send_command("show ip route")
)


print("\n========================================")
print("OSPF")
print("========================================")

print(
    connection.send_command("show ip protocols")
)


print("\n========================================")
print("OSPF NEIGHBORS")
print("========================================")

print(
    connection.send_command("show ip ospf neighbor")
)


print("\n========================================")
print("RUNNING CONFIGURATION")
print("========================================")

print(
    connection.send_command("show running-config")
)


# ============================================================
# DISCONNECT
# ============================================================

connection.disconnect()

print("\nDisconnected.")