import os
import csv
import random

# Constants
BASE_DIR = r"C:\Masonry\A\Data"
ROOM_DIMENSIONS = {
    "width": (15, 30, 5),
    "length": (15, 30, 5)
}
WALL_THICKNESS_RANGES = {
    "inner": (1, 2, 0.5),
    "outer": (2, 4, 0.5),
    "hall": (15, 30, 5)
}

def ensure_directory():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def generate_unique_filename(index):
    return os.path.join(BASE_DIR, f"{index}.csv")

def generate_random_value(start, end, step):
    return round(random.uniform(start, end) / step) * step

def generate_rooms(num_bedrooms, num_bathrooms):
    rooms = []

    # Ensure the first column is always a Bedroom
    rooms.append(f"BE1")
    
    # Add bedrooms and bathrooms
    for i in range(num_bedrooms):
        if i > 0:  # Skip the first bedroom as it's already added
            rooms.append(f"BE{i + 1}")
        # Insert a bathroom immediately after each bedroom
        if i < num_bathrooms:  # Ensure not to exceed bathroom count
            rooms.append(f"BA{i + 1}")  # Add bathroom
        
    # Add remaining bathrooms if needed
    for i in range(num_bathrooms - num_bedrooms):
        rooms.append(f"BA{num_bedrooms + i + 1}")

    # Randomize the order of rooms while maintaining the pairing
    random.shuffle(rooms[1:])  # Shuffle everything except the first Bedroom

    # Ensure the last column is a bathroom if there's an odd count of bedrooms
    if rooms[-1].startswith("BE"):
        rooms.append(f"BA{num_bathrooms}")  # Append one more bathroom if last is a bedroom

    return rooms

def generate_wall_thickness_values():
    return {
        "inner": generate_random_value(*WALL_THICKNESS_RANGES["inner"]),
        "outer": generate_random_value(*WALL_THICKNESS_RANGES["outer"]),
        "hall": generate_random_value(*WALL_THICKNESS_RANGES["hall"]),
    }

def create_floor_plan_file(file_index):
    ensure_directory()
    filename = generate_unique_filename(file_index)
    
    # Determine random number of bedrooms and bathrooms
    num_bedrooms = random.randint(1, 3)
    num_bathrooms = random.randint(num_bedrooms, 2 * num_bedrooms)  # Ensure at least 1 bathroom per bedroom
    
    print(f"Generating file {filename} with {num_bedrooms} bedrooms and {num_bathrooms} bathrooms.")
    
    # Generate room sequence
    rooms = generate_rooms(num_bedrooms, num_bathrooms)
    wall_thickness = generate_wall_thickness_values()
    
    data = []
    for room in rooms:
        width = generate_random_value(*ROOM_DIMENSIONS["width"])
        length = generate_random_value(*ROOM_DIMENSIONS["length"])
        data.append([width, length, room])
    
    # Append hall, inner wall, and outer wall data
    data.append(["Hall Thickness", wall_thickness["hall"]])
    data.append(["Inner Wall Thickness", wall_thickness["inner"]])
    data.append(["Outer Wall Thickness", wall_thickness["outer"]])
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main(number_of_files):
    for i in range(1, number_of_files + 1):
        create_floor_plan_file(i)

if __name__ == "__main__":
    # Change the number of files to generate here
    main(10)
