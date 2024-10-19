import os
import csv
import random

# Constants
BASE_DIR = r"C:\Masonry\A\Data"
MIN_COLUMNS = 3
MAX_COLUMNS = 18
WEIGHTED_COLUMN_RANGES = [(3, 9), (10, 15), (16, 18)]
WEIGHTED_PROBABILITIES = [0.6, 0.3, 0.1]
ROOM_TYPES = {
    "BA": (1, 6),
    "BE": (1, 3),
    "KI": (1, 3),
    "LI": (1, 3),
    "GA": (1, 3)
}
ROOM_DIMENSIONS = {
    "width": (25, 75, 5),
    "length": (25, 75, 5)
}
WALL_THICKNESS_RANGES = {
    "inner": (1, 2, 0.5),
    "outer": (2, 4, 0.5),
    "hall": (10, 25, 5)
}

def ensure_directory():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def generate_unique_filename(index):
    return os.path.join(BASE_DIR, f"{index}.csv")

def select_number_of_columns():
    range_choice = random.choices(WEIGHTED_COLUMN_RANGES, WEIGHTED_PROBABILITIES)[0]
    return random.randint(range_choice[0], range_choice[1])

def generate_random_value(start, end, step):
    return round(random.uniform(start, end) / step) * step

def is_valid_placement(room_type, previous_room):
    if previous_room is None:
        return True
    # Bathroom constraints
    if room_type == "BA" and previous_room[:2] in {"KI", "GA", "LI"}:
        return False
    # Bedroom constraints
    if room_type == "BE" and previous_room[:2] == "GA":
        return False
    # Garage constraints
    if room_type == "GA" and previous_room[:2] == "BA":
        return False
    return True

def is_valid_sequence(sequence):
    for i in range(1, len(sequence)):
        current_room = sequence[i][:2]
        previous_room = sequence[i - 1][:2]
        # Enforce rules for bathrooms, bedrooms, and garages adjacency
        if current_room == "BA" and previous_room in {"KI", "GA", "LI"}:
            return False
        if previous_room == "BA" and current_room in {"KI", "GA", "LI"}:
            return False
        if current_room == "BE" and previous_room == "GA":
            return False
        if previous_room == "BE" and current_room == "GA":
            return False
    return True

def place_garages(rooms, max_columns):
    # Ensure garages are placed correctly according to rules
    garages = [room for room in rooms if room.startswith("GA")]
    non_garages = [room for room in rooms if not room.startswith("GA")]
    
    # Garage placement rules
    if garages:
        first_garage = garages[0]
        remaining_garages = garages[1:]
        
        # Place the first garage in the first column
        result = [first_garage]
        # Place the remaining rooms
        result.extend(non_garages)
        
        # If there are additional garages, add them to the end
        if remaining_garages:
            result.extend(remaining_garages)
    else:
        result = non_garages
    
    return result

def generate_room_sequence(num_columns):
    rooms = []
    available_rooms = {k: v[0] for k, v in ROOM_TYPES.items()}
    used_counts = {k: 0 for k in ROOM_TYPES}
    
    # Populate rooms while ensuring mandatory room types are included
    while len(rooms) < num_columns - 3:  # Reserve the last three columns for wall data
        room_type = random.choice(list(available_rooms.keys()))
        if used_counts[room_type] < ROOM_TYPES[room_type][1]:
            if len(rooms) == 0 or is_valid_placement(room_type, rooms[-1]):
                used_counts[room_type] += 1
                rooms.append(f"{room_type}{used_counts[room_type]}")

    # Ensure there is at least one bathroom, one bedroom, and one kitchen
    mandatory_rooms = ["BA1", "BE1", "KI1"]
    for room in mandatory_rooms:
        if room not in rooms:
            rooms.append(room)

    # Adjust garages placement according to rules
    rooms = place_garages(rooms, num_columns)

    # Shuffle until a valid sequence is found that respects adjacency rules
    max_attempts = 1000
    attempts = 0
    while not is_valid_sequence(rooms):
        if attempts >= max_attempts:
            print(f"Unable to find a valid sequence after {attempts} attempts. Retrying...")
            rooms = place_garages(rooms, num_columns)
            attempts = 0
        random.shuffle(rooms)
        attempts += 1
        if attempts % 100 == 0:
            print(f"Attempt {attempts}: Still trying to find a valid sequence...")
    
    print(f"Valid sequence found after {attempts} attempts.")
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
    num_columns = select_number_of_columns()
    print(f"Generating file {filename} with {num_columns} columns.")
    rooms = generate_room_sequence(num_columns)
    wall_thickness = generate_wall_thickness_values()
    
    data = []
    for i, room in enumerate(rooms):
        width = generate_random_value(*ROOM_DIMENSIONS["width"])
        length = generate_random_value(*ROOM_DIMENSIONS["length"])
        data.append([width, length, room])
    
    # Append hall, inner wall, and outer wall data without leading ","
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
    main(2)
