network_info = ("Router: Cisco, IP: 192.168.1.1")
print(network_info )

# Write network intofrmation to a file
file = open('network_report.txt', 'w')
file.write(network_info)
file.close()

# Read the network information back from the file
file = open("network_report.txt", 'r')
content = file.read()
print (content)
file.close()

