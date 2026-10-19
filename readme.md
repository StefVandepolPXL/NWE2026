* Switch
```bash
enable
configure terminal
hostname SW1
ip domain name data.labnet.local
no ip domain lookup
crypto key generate rsa modulus 2048
ip ssh version 2
username student privilege 15 secret pxl
line vty 0 15
 transport input ssh
 login local
exit

ip default-gateway 172.16.17.2

vlan 117
 name management
vlan 99
 name native
exit

interface vlan 117
 ip address 172.16.17.4 255.255.255.192
 no shutdown
exit

interface gigabitEthernet 1/0/1
 switchport mode access
 switchport access vlan 117
 spanning-tree portfast
exit

interface gigabitEthernet 1/0/2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 99,117
 spanning-tree link-type point-to-point
 no shutdown
exit

```
* Router
```bash
enable
configure terminal
hostname R1
ip domain name data.labnet.local
no ip domain lookup
crypto key generate rsa modulus 2048
ip ssh version 2
username student privilege 15 secret pxl
line vty 0 15
 transport input ssh
 login local
exit

interface gigabitEthernet 0/0/0
 no ip address
 no shutdown
exit

interface gigabitEthernet 0/0/0.99
 encapsulation dot1Q 99 native
exit

interface gigabitEthernet 0/0/0.117
 encapsulation dot1Q 117
 ip address 172.16.17.2 255.255.255.192
exit
```

```bash
 New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 172.16.17.10 -PrefixLength 26 -DefaultGateway 172.16.17.2
```



goodluck tijger