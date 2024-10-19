import os
from pyautocad import Autocad, APoint
import csv

# Initialize AutoCAD
acad = Autocad(create_if_not_exists=True)

# File path of the CSV on Windows
csv_file_path = 'C:\\data\\1.csv'

# Directory for output files
output_directory = 'C:\\data\\designs'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Scaling factor (100000 as requested)
scaling_factor = 100000

# Read the layout from the CSV
def read_layout(file_path):
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        data = list(csv_reader)

    rooms = []
    inner_wall_thickness = None
    outer_wall_thickness = None

    for row in data:
        if row[0].startswith('Inner Wall Thickness'):
            inner_wall_thickness = float(row[1])
        elif row[0].startswith('Outer Wall Thickness'):
            outer_wall_thickness = float(row[1])
        else:
            length = float(row[0])
            width = float(row[1])
            name = row[2]
            door = row[3]
            window = row[4]
            rooms.append((length, width, name, door, window))

    return rooms, inner_wall_thickness, outer_wall_thickness

# Function to draw room with outer and inner walls
def draw_room_with_walls(start_point, length, width, name, door, window, inner_wall_thickness, outer_wall_thickness):
    try:
        # Apply scaling
        length *= scaling_factor
        width *= scaling_factor
        inner_wall_thickness *= scaling_factor
        outer_wall_thickness *= scaling_factor

        # Adjust the points to draw walls outside room dimensions
        outer_p1 = APoint(start_point[0] - outer_wall_thickness, start_point[1] + outer_wall_thickness)
        outer_p2 = APoint(start_point[0] + length + outer_wall_thickness, start_point[1] + outer_wall_thickness)
        outer_p3 = APoint(start_point[0] + length + outer_wall_thickness, start_point[1] - width - outer_wall_thickness)
        outer_p4 = APoint(start_point[0] - outer_wall_thickness, start_point[1] - width - outer_wall_thickness)

        # Draw outer walls
        acad.model.AddLine(outer_p1, outer_p2)
        acad.model.AddLine(outer_p2, outer_p3)
        acad.model.AddLine(outer_p3, outer_p4)
        acad.model.AddLine(outer_p4, outer_p1)

        # Draw the inner walls as well outside the room dimensions
        inner_p1 = APoint(start_point[0] - inner_wall_thickness, start_point[1] + inner_wall_thickness)
        inner_p2 = APoint(start_point[0] + length + inner_wall_thickness, start_point[1] + inner_wall_thickness)
        inner_p3 = APoint(start_point[0] + length + inner_wall_thickness, start_point[1] - width - inner_wall_thickness)
        inner_p4 = APoint(start_point[0] - inner_wall_thickness, start_point[1] - width - inner_wall_thickness)

        # Draw inner walls
        acad.model.AddLine(inner_p1, inner_p2)
        acad.model.AddLine(inner_p2, inner_p3)
        acad.model.AddLine(inner_p3, inner_p4)
        acad.model.AddLine(inner_p4, inner_p1)

        # Add room name and dimensions (only one)
        acad.model.AddText(f"{name}\n{length/scaling_factor}x{width/scaling_factor}",
                           APoint(start_point[0] + length / 2, start_point[1] - width / 2), 3 * scaling_factor)

        # Add doors as part of the hall
        if door == 'door':
            acad.model.AddLine(APoint(start_point[0] + 2 * scaling_factor, start_point[1]),
                               APoint(start_point[0] + 5 * scaling_factor, start_point[1]))  # Door on top wall

        # Add double windows to each room
        if window == 'window':
            acad.model.AddLine(APoint(start_point[0], start_point[1] - width / 2),
                               APoint(start_point[0] + length / 2, start_point[1] - width / 2))  # Window side 1
            acad.model.AddLine(APoint(start_point[0] + length / 2, start_point[1] - width / 2),
                               APoint(start_point[0] + length, start_point[1] - width / 2))  # Window side 2

    except Exception as e:
        print(f"Error drawing room: {name}. Error: {str(e)}")

# Function to draw rooms with walls
def draw_rooms(file_path, output_directory):
    rooms, inner_wall, outer_wall = read_layout(file_path)

    x_offset = 0
    hall_width = 10 * scaling_factor  # Width of the hall separating rooms

    # Drawing the rooms
    for i, (length, width, name, door, window) in enumerate(rooms):
        # Coordinates for the room
        start_point = (x_offset, 0)

        # Draw the room with inner and outer walls
        draw_room_with_walls(start_point, length, width, name, door, window, inner_wall, outer_wall)

        # Update x_offset for the next room
        x_offset += (length + 5) * scaling_factor  # Add some spacing between rooms

    # Save the drawing to the designs folder
    output_file = os.path.join(output_directory, "layout.dwg")
    acad.doc.SaveAs(output_file)
    print(f"Drawing saved to: {output_file}")

# Call the function to draw rooms and save the output
draw_rooms(csv_file_path, output_directory)
