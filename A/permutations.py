import random
import csv
import os

# Define the available dimensions for each room type
bedroom_dimensions = [35, 40, 45, 50]
bathroom_dimensions = [35, 40, 45, 50]
living_room_dimensions = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150]
kitchen_dimensions = living_room_dimensions
garage_dimensions = living_room_dimensions

# Set the wall thicknesses in increments of 0.5
inner_wall_thickness = [1.5, 2.0, 2.5, 3.0]
outer_wall_thickness = [3.0, 3.5, 4.0, 4.5, 5.0]

# Max number of lines per file
max_files_to_create = 37029000  # Desired number of files

def generate_layout():
    layout = []
    bedroom_count = random.randint(1, 5)
    bathroom_count = random.randint(1, 5)
    kitchen_count = random.randint(1, 3)
    garage_count = random.randint(1, 2)
    living_room_count = random.randint(1, 5)

    bedrooms = [[random.choice(bedroom_dimensions), random.choice(bedroom_dimensions), f"Bedroom {i+1}", "door", "window"] for i in range(bedroom_count)]
    bathrooms = [[random.choice(bathroom_dimensions), random.choice(bathroom_dimensions), f"Bathroom {i+1}", "door", "window"] for i in range(bathroom_count)]
    kitchens = [[random.choice(kitchen_dimensions), random.choice(kitchen_dimensions), f"Kitchen {i+1}", "door", "no window"] for i in range(kitchen_count)]
    garages = [[random.choice(garage_dimensions), random.choice(garage_dimensions), f"Garage {i+1}", "door", "no window"] for i in range(garage_count)]
    living_rooms = [[random.choice(living_room_dimensions), random.choice(living_room_dimensions), f"Living Room {i+1}", "door", "window"] for i in range(living_room_count)]

    # Ensure that bedrooms and bathrooms are together in the layout
    layout.extend(bedrooms)
    layout.extend(bathrooms)

    # Decide whether to place living rooms before or after bedrooms and bathrooms
    living_rooms_on_left = random.choice([True, False])

    if living_rooms_on_left:
        layout = living_rooms + layout  # Living rooms on the left
    else:
        layout = layout + living_rooms  # Living rooms on the right

    # If living rooms are in the middle, separate with kitchen or garage
    if len(bedrooms) > 0 and len(bathrooms) > 0 and len(living_rooms) > 0:
        if living_rooms_on_left:
            layout.append(kitchens[0]) if kitchens else layout.append(garages[0])
        else:
            layout.insert(0, kitchens[0]) if kitchens else layout.insert(0, garages[0])

    # Add garages and kitchens if not added yet
    if kitchens and kitchens[0] not in layout:
        layout.append(kitchens[0])
    if garages and garages[0] not in layout:
        layout.append(garages[0])

    inner_wall = random.choice(inner_wall_thickness)
    outer_wall = random.choice(outer_wall_thickness)

    return layout, inner_wall, outer_wall

def generate_unique_file_name(file_counter, base_file_path):
    """
    Generate a unique file name using the counter and return the full path.
    """
    file_name = f"{file_counter}.csv"
    file_path = os.path.join(base_file_path, file_name)

    return file_path

def write_layout_to_csv(base_file_path):
    file_counter = 1  # Start counter at 1

    # Ensure the base directory exists
    os.makedirs(base_file_path, exist_ok=True)

    while file_counter <= max_files_to_create:
        layout, inner_wall, outer_wall = generate_layout()

        # Generate a unique file name based on the counter
        file_path = generate_unique_file_name(file_counter, base_file_path)
        
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w', newline='') as current_file:
            writer = csv.writer(current_file)
            
            # Write the layout to the current file
            for room in layout:
                writer.writerow(room)
            writer.writerow(["Inner Wall Thickness", inner_wall])
            writer.writerow(["Outer Wall Thickness", outer_wall])
        
        print(f"Finished writing {file_path}")

        file_counter += 1  # Increment counter for the next file

        # Stop after reaching the desired number of files
        if file_counter > max_files_to_create:
            print(f"Reached target of {max_files_to_create} files. Stopping.")
            break

# Example usage
write_layout_to_csv('/mnt/c/A/Halls')
