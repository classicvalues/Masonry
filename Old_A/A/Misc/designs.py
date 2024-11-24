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

# Function to manually draw room walls using AddLine
def draw_room(start_point, length, width, name, dimensions, door, window, inner_wall, outer_wall):
    try:
        # Apply scaling
        length *= scaling_factor
        width *= scaling_factor

        # Define the four corners of the outer room
        p1 = APoint(start_point[0], start_point[1])
        p2 = APoint(start_point[0] + length, start_point[1])
        p3 = APoint(start_point[0] + length, start_point[1] - width)
        p4 = APoint(start_point[0], start_point[1] - width)

        # Draw the outer walls
        acad.model.AddLine(p1, p2)  # Top wall
        acad.model.AddLine(p2, p3)  # Right wall
        acad.model.AddLine(p3, p4)  # Bottom wall
        acad.model.AddLine(p4, p1)  # Left wall

        # Define the four corners of the inner room
        inner_p1 = APoint(start_point[0] + inner_wall, start_point[1] - inner_wall)
        inner_p2 = APoint(start_point[0] + length - inner_wall, start_point[1] - inner_wall)
        inner_p3 = APoint(start_point[0] + length - inner_wall, start_point[1] - width + inner_wall)
        inner_p4 = APoint(start_point[0] + inner_wall, start_point[1] - width + inner_wall)

        # Draw the inner walls
        acad.model.AddLine(inner_p1, inner_p2)  # Inner top wall
        acad.model.AddLine(inner_p2, inner_p3)  # Inner right wall
        acad.model.AddLine(inner_p3, inner_p4)  # Inner bottom wall
        acad.model.AddLine(inner_p4, inner_p1)  # Inner left wall

        # Center the room name and dimensions only once
        text_x_offset = length / 2  # Center text horizontally
        text_y_offset = width / 2
        acad.model.AddText(f"{name}", APoint(start_point[0] + text_x_offset, start_point[1] - text_y_offset), 3 * scaling_factor)
        acad.model.AddText(f"{dimensions}", APoint(start_point[0] + text_x_offset, start_point[1] - text_y_offset - 5 * scaling_factor), 2 * scaling_factor)

        # Add the door
        if door == 'door':
            door_width = 3 * scaling_factor  # 3 feet door width
            door_height = 1 * scaling_factor  # Height is not considered in 2D
            
            # Position the door 12 inches (1 foot) from the wall
            door_start = APoint(start_point[0] + length / 2 - door_width / 2, start_point[1] + 1 * scaling_factor)
            door_end = APoint(start_point[0] + length / 2 + door_width / 2, start_point[1] + 1 * scaling_factor)
            
            # Draw the door frame
            acad.model.AddLine(door_start, door_end)  # Door width
            
            # Draw the door swing lines
            line_45 = APoint(start_point[0] + length / 2 + 1 * scaling_factor, start_point[1] + door_width / 2 + 1 * scaling_factor)
            line_90 = APoint(start_point[0] + length / 2 + 1 * scaling_factor + door_width / 2, start_point[1] + door_width / 2 + 1 * scaling_factor)
            acad.model.AddLine(door_start, line_45)  # 45 degrees line
            acad.model.AddLine(door_start, line_90)  # 90 degrees line
            
            # Draw arc for the door swing
            acad.model.AddArc(door_start, door_width / 2, 0, 45)  # Arc from 0 to 45 degrees
            acad.model.AddArc(door_start, door_width / 2, 45, 180)  # Arc from 45 to 180 degrees
            
            # No need to delete lines as they're not used

        # Add the window
        if window == 'window':
            window_thickness = 0.5 * outer_wall * scaling_factor
            window_start_20 = APoint(start_point[0] + (0.2 * length), start_point[1] - (0.5 * width))
            window_start_80 = APoint(start_point[0] + (0.8 * length), start_point[1] - (0.5 * width))
            window_middle = APoint(start_point[0] + length / 2, start_point[1] - (0.5 * width))

            # Draw window lines
            acad.model.AddLine(window_start_20, window_middle)
            acad.model.AddLine(window_start_80, window_middle)
            acad.model.AddLine(window_middle, APoint(window_start_20[0], window_start_80[1]))  # Horizontal line
            
            # Draw cross lines
            acad.model.AddLine(window_start_20, APoint(window_start_20[0] + window_thickness, window_start_20[1]))
            acad.model.AddLine(window_start_80, APoint(window_start_80[0] - window_thickness, window_start_80[1]))

    except Exception as e:
        print(f"Error drawing room: {name}. Error: {str(e)}")

# Draw all rooms and save the output to a file in the designs folder
def draw_rooms(file_path, output_directory):
    rooms, inner_wall, outer_wall = read_layout(file_path)
    
    x_offset = 0
    hall_width = 10 * scaling_factor  # Width of the hall separating the two rows of rooms
    mirrored_x_offset = len(rooms) * 50 * scaling_factor + hall_width  # Distance for mirrored rooms on the other side

    # Drawing the rooms
    for i, (length, width, name, door, window) in enumerate(rooms):
        # Coordinates for the first row of rooms
        start_point = (x_offset, 0)
        
        # Draw the room
        draw_room(start_point, length, width, name, f"{length}x{width}", door, window, inner_wall, outer_wall)
        
        # Coordinates for the mirrored room on the opposite side of the hall
        mirrored_start_point = (x_offset, -width - hall_width)
        
        # Draw the mirrored room
        draw_room(mirrored_start_point, length, width, name, f"{length}x{width}", door, window, inner_wall, outer_wall)

        # Update x_offset for the next room
        x_offset += (length + 5) * scaling_factor  # Add some spacing between rooms

    # Save the drawing to the designs folder
    output_file = os.path.join(output_directory, "layout.dwg")
    acad.doc.SaveAs(output_file)
    print(f"Drawing saved to: {output_file}")

# Call the function to draw rooms and save the output
draw_rooms(csv_file_path, output_directory)
