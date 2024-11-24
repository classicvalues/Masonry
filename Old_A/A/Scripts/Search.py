import os
import csv

# Constants
BASE_DIR = r"C:\Masonry\A\Data"
FILE_LIMIT = 50

def get_room_preferences():
    room_types = {
        "bedrooms": (1, 3),
        "bathrooms": (1, 6),
        "kitchens": (1, 3),
        "living rooms": (1, 3),
        "garages": (1, 3)
    }
    preferences = {}
    
    for room, (min_val, max_val) in room_types.items():
        while True:
            user_input = input(f"How many {room} (from {min_val} to {max_val}, or type 'I do not know')? ")
            if user_input.lower() == "i do not know":
                preferences[room] = None
                break
            elif user_input.isdigit() and min_val <= int(user_input) <= max_val:
                preferences[room] = int(user_input)
                break
            else:
                print(f"Please enter a number between {min_val} and {max_val}, or 'I do not know'.")

    # Get room size preference
    room_size = input("Do you prefer small (35x35-45x45), medium (45x45-55x55), or large (55x55-75x75) rooms? ").lower()
    preferences['room_size'] = room_size if room_size in {"small", "medium", "large"} else None

    # Get hall width preference
    hall_width = input("Do you prefer small (10-15), medium (15-20), or large (20-25) halls? ").lower()
    preferences['hall_width'] = hall_width if hall_width in {"small", "medium", "large"} else None

    # Get layout preference
    layout_preference = input("Do you prefer a 'spacey' or 'homely' layout? ").lower()
    preferences['layout'] = layout_preference if layout_preference in {"spacey", "homely"} else None
    
    return preferences

def parse_file_metadata(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        rooms = []
        hall_thickness = None
        inner_wall_thickness = None
        outer_wall_thickness = None
        for row in reader:
            if len(row) == 3:
                rooms.append(row[2])
            elif len(row) == 2:
                if "Hall" in row[0]:
                    hall_thickness = int(row[1])
                elif "Inner" in row[0]:
                    inner_wall_thickness = float(row[1])
                elif "Outer" in row[0]:
                    outer_wall_thickness = float(row[1])
        return {
            "rooms": rooms,
            "hall_thickness": hall_thickness,
            "inner_wall_thickness": inner_wall_thickness,
            "outer_wall_thickness": outer_wall_thickness
        }

def match_preferences(metadata, preferences):
    score = 0
    
    # Count room types
    room_counts = {room_type: 0 for room_type in ["BE", "BA", "KI", "LI", "GA"]}
    for room in metadata["rooms"]:
        room_type = room[:2]
        room_counts[room_type] += 1
    
    # Match room counts if specified
    for room_type, count in preferences.items():
        if room_type in room_counts and count is not None:
            if room_counts[room_type[:2]] == count:
                score += 10

    # Match room size preference
    if preferences['room_size']:
        size_ranges = {"small": (35, 45), "medium": (45, 55), "large": (55, 75)}
        matched = False
        for room in metadata["rooms"]:
            # Assuming room dimensions are stored as 'width,length,room_name'
            parts = room.split(',')
            if len(parts) >= 2:
                try:
                    width = int(parts[0])
                    length = int(parts[1])
                    room_size_range = size_ranges[preferences['room_size']]
                    if room_size_range[0] <= width <= room_size_range[1] and room_size_range[0] <= length <= room_size_range[1]:
                        matched = True
                        break
                except ValueError:
                    # Skip if conversion fails (e.g., if it's the room identifier)
                    continue
        if matched:
            score += 5

    # Match hall width preference
    hall_width_ranges = {"small": (10, 15), "medium": (15, 20), "large": (20, 25)}
    if preferences['hall_width']:
        hall_range = hall_width_ranges[preferences['hall_width']]
        if hall_range[0] <= metadata["hall_thickness"] <= hall_range[1]:
            score += 3

    # Match layout preference (spacey or homely)
    if preferences['layout']:
        first_half_rooms = metadata["rooms"][:len(metadata["rooms"]) // 2]
        count_bedrooms = sum(1 for room in first_half_rooms if room.startswith("BE"))
        count_living_rooms = sum(1 for room in first_half_rooms if room.startswith("LI"))
        
        if preferences['layout'] == "spacey" and count_living_rooms > count_bedrooms:
            score += 7
        elif preferences['layout'] == "homely" and count_bedrooms > count_living_rooms:
            score += 7
    
    return score

def search_floor_plans(preferences):
    files = [f for f in os.listdir(BASE_DIR) if f.endswith(".csv")]
    results = []

    for file in files:
        filepath = os.path.join(BASE_DIR, file)
        metadata = parse_file_metadata(filepath)
        score = match_preferences(metadata, preferences)
        results.append((file, score))

    # Sort results by score, descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:FILE_LIMIT]

def main():
    preferences = get_room_preferences()
    results = search_floor_plans(preferences)
    if results:
        print(f"Top {len(results)} relevant files based on your preferences:")
        for filename, score in results:
            print(f"File: {filename}, Score: {score}")
    else:
        print("No relevant files found.")

if __name__ == "__main__":
    main()
