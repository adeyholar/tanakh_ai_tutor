# Create Network Equipment Data File
network_devices = ("Router: Cisco\nSwich: Netgear\nFirewall: SonicWall")
print(network_devices)

# Write Network Equipment Data to a file
file = open ('network_devices.txt', 'w')
file.write (network_devices)
file.close()

# Read the Network Equipment Data back from the file
file = open ("network_devices.txt", 'r')
content = file.read()
print("\n====📄 Network Devices Report:=====")
print(content)
file.close()