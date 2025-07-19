farm_equipment = ("Tractor: John Deere 5075E\nLast Service: 2025-06-15\nHours: 1,250\nStatus: Operational,\nCombine: Case IH 2150 Series\nLast Service: 2025-05-20\nHours: 845\nStatus: Needs Oil Change,\nHarvester: New Holland CR9.90\nLast Service: 2025-07-10\nHours: 1,500\nStatus: Operational,\nSeeder: Great Plains 3P606NT\nLast Service: 2025-04-30\nHours: 600\nStatus: Operational,\nPlanter: Kinze 4900\nLast Service: 2025-03-15\nHours: 520\nStatus: Operational")
print ("========================================================")
print ("Farm Equipment Status Report")
print ("========================================================")
print (farm_equipment)

# Write farm equipment data to a file
file = open("farm_equipments.txt", "w")
file.write (farm_equipment)
file.close()

# Read the farm equipment data back from the file
file = open("farm_equipments.txt", "r")
content = file.read()
print("\n====📄 Farm Equipment Report:=====")
print(content)
file.close()

# Append new equipment data to the file
file = open("farm_equipments.txt", "a")
new_equipment = ("\n\nSprayer: Apache 1020\nLast Service: 2025-07-01\nHours: 300\nStatus: Operational")
file.write(new_equipment)
file.close()