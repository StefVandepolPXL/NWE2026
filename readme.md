```bash
ip domain name data.labnet.local
crypto key generate rsa
yes

username admin privilege 15 secret cisco
line vty 0 15
transport input ssh
login local
exit

interface gigabitEthernet 0/0/0
ip address 172.16.16.2 255.255.255.192
no shutdown
```

```bash
 New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 172.16.16.10 -PrefixLength 26 -DefaultGateway 172.16.16.2
```

goodluck tijger