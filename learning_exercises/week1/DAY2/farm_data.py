# farm_data.py - Week 1 Day 2: Working with Files
# SIMPLE and PRACTICAL examples

def create_farm_data_file():
    """Create a simple file with farm data"""
    
    # This is just a string with farm information
    farm_data = """Crop: Corn
Acres: 150
Plant Date: 2025-03-15
Expected Harvest: 2025-09-30
Notes: Good soil conditions"""
    
    # Write this string to a file
    with open('farm_report.txt', 'w') as file:
        file.write(farm_data)
    
    print("✅ Created farm_report.txt")

def read_farm_data_file():
    """Read the farm data back from the file"""
    
    # Read the entire file content
    with open('farm_report.txt', 'r') as file:
        content = file.read()
    
    print("📄 File contents:")
    print(content)
    
    return content

# Let's use these functions
if __name__ == "__main__":
    print("🚜 FARM DATA FILE DEMO")
    print("=" * 30)
    
    # Step 1: Create the file
    create_farm_data_file()
    
    # Step 2: Read it back
    data = read_farm_data_file()    