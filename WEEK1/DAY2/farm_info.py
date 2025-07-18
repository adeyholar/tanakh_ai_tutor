# Start with just creating the data in memory.
farm_info = "Crop: Corn, Acres: 150"
print(farm_info)

file = open ('test.txt', 'w')
file.write("Hellof from my farm")
file.close()
