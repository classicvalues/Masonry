import csv
import os
import random

# Function to parse input CSV
def parse_input_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    
    hall_thickness = float([row[1] for row in data if row[0] == 'Hall Thickness'][0])
    inner_wall_thickness = float([row[1] for row in data if row[0] == 'Inner Wall Thickness'][0])
    outer_wall_thickness = float([row[1] for row in data if row[0] == 'Outer Wall Thickness'][0])
    rooms = [row for row in data if row[0] not in ['Hall Thickness', 'Inner Wall Thickness', 'Outer Wall Thickness']]
    
    return rooms, hall_thickness, inner_wall_thickness, outer_wall_thickness

# Function to generate living room, kitchen, and garage sizes
def generate_living_room_size(rooms, hall_thickness, inner_wall_thickness):
    first_bedroom_length = int(rooms[0][0])
    total_size = first_bedroom_length * 2 + hall_thickness + (2 * inner_wall_thickness)
    return random.randint(int(total_size), int(total_size) + 20)

# Function to determine the hallway descriptor (top, bottom, left, or right)
def determine_hallway_descriptor(rooms):
    if rooms[0][2].startswith('BE') and rooms[-1][2].startswith('BE'):
        return 'left'  # No top or bottom, as BE is on both sides
    return random.choice(['top', 'bottom'])

# Function to generate variations
def generate_variations(base_file_path, output_folder, num_variations=10):
    rooms, hall_thickness, inner_wall_thickness, outer_wall_thickness = parse_input_csv(base_file_path)
    base_file_name = os.path.basename(base_file_path).split('.')[0]
    
    for i in range(1, num_variations + 1):
        living_room_size = generate_living_room_size(rooms, hall_thickness, inner_wall_thickness)
        kitchen_size = living_room_size
        garage_size = living_room_size
        
        # Randomly decide the configuration (single or double)
        configuration = random.choice(['single', 'double'])
        hall_descriptor = determine_hallway_descriptor(rooms) if configuration == 'double' else 'single'
        
        # Create the new layout based on the configuration
        new_layout = rooms.copy()
        new_layout.append([f"Living Room {configuration} ({hall_descriptor})", living_room_size, living_room_size])
        new_layout.append([f"Kitchen {configuration}", kitchen_size, kitchen_size])
        new_layout.append([f"Garage {configuration}", garage_size, garage_size])
        
        # Append wall thickness details at the end
        new_layout.append(['Hall Thickness', hall_thickness])
        new_layout.append(['Inner Wall Thickness', inner_wall_thickness])
        new_layout.append(['Outer Wall Thickness', outer_wall_thickness])
        
        # Write to new CSV file
        output_file_name = f"{base_file_name}-{i}.csv"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        with open(output_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_layout)

# Function to process all files in the directory
def process_all_files(input_folder, output_folder, num_variations=10):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            base_file_path = os.path.join(input_folder, file_name)
            generate_variations(base_file_path, output_folder, num_variations)

# Main function
def main():
    input_folder = "C:\\Masonry\\A\\Data"
    output_folder = "C:\\Masonry\\A\\Data\\Homes"
    num_variations = 10
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    process_all_files(input_folder, output_folder, num_variations)

if __name__ == "__main__":
    main()
