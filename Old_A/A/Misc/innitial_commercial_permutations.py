import random
import csv
import os

# Define dimensions for all rooms (identical range)
room_dimensions = [i for i in range(20, 101, 5)]

# Bathroom and entrance living room must have identical dimensions between 75 and 100
bathroom_living_room_dimensions = [75, 80, 85, 90, 95, 100]

# Max number of lines per file
max_files_to_create = 1000  # Adjust this as needed

def generate_layout_with_living_and_bathroom(n_rooms):
    # Ensure n_rooms is at least 5, with 1 living room and 1 bathroom
    assert n_rooms >= 5, "Number of rooms must be at least 5"

    # Create a list for the layout
    layout = []

    # First, create the entrance living room and bathroom
    room_size = random.choice(bathroom_living_room_dimensions)
    living_room = [room_size, room_size, "Living Room (Entrance)", "door", "wall"]
    bathroom = [room_size, room_size, "Bathroom (End)", "door", "wall"]

    # Add both living room and bathroom
    layout.append(living_room)

    # Now create identical regular rooms with windows
    for i in range(n_rooms - 2):  # Subtract 2 for living room and bathroom
        room_size = random.choice(room_dimensions)
        layout.append([room_size, room_size, f"Room {i + 1}", "window", "window"])

    layout.append(bathroom)

    return layout

def generate_layout_without_living_and_bathroom(n_rooms):
    layout = []
    for i in range(n_rooms):  # No living room or bathroom
        room_size = random.choice(room_dimensions)
        layout.append([room_size, room_size, f"Room {i + 1}", "window", "window"])

    return layout

def generate_file_name(n_rooms, has_living_bathroom, base_file_path):
    """
    Generate a unique file name based on number of rooms and presence of living room/bathroom.
    """
    if has_living_bathroom:
        file_name = f"{n_rooms}_rooms_with_LR_and_B.csv"
    else:
        file_name = f"{n_rooms}_rooms_no_LR_B.csv"

    return os.path.join(base_file_path, file_name)

def write_layout_to_csv(base_file_path):
    file_counter = 1  # Start counter at 1
    os.makedirs(base_file_path, exist_ok=True)

    while file_counter <= max_files_to_create:
        # Randomly choose number of rooms between 5 and 150
        n_rooms = random.randint(5, 150)

        # Generate layout with living room and bathroom
        layout_with_lr_and_bathroom = generate_layout_with_living_and_bathroom(n_rooms)
        file_name = generate_file_name(n_rooms, True, base_file_path)

        # Write the layout with living room and bathroom
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for room in layout_with_lr_and_bathroom:
                writer.writerow(room)

        print(f"Finished writing layout with living room and bathroom: {file_name}")

        # Generate layout without living room and bathroom (same room count)
        layout_without_lr_and_bathroom = generate_layout_without_living_and_bathroom(n_rooms)
        file_name_r = file_name.replace('.csv', 'r.csv')

        # Write the layout without living room and bathroom
        with open(file_name_r, 'w', newline='') as csv_file_r:
            writer = csv.writer(csv_file_r)
            for room in layout_without_lr_and_bathroom:
                writer.writerow(room)

        print(f"Finished writing layout without living room and bathroom: {file_name_r}")

        file_counter += 1

# Example usage
write_layout_to_csv('/mnt/c/A/Halls')
