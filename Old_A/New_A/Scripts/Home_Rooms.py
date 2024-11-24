import pandas as pd
import os

# Initialize an empty list to store room dimensions
room_dimensions = []

# Define the room dimensions
lengths = [36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180]  # Lengths
widths = [36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180]   # Widths
heights = [12, 18, 24]  # Heights

# Define the wall widths
inner_wall_widths = [0.5, 1, 1.5, 2]  # Inner Wall Widths
outer_wall_widths = [1, 1.5, 2, 2.5, 3, 3.5, 4]  # Outer Wall Widths

# Define the attachment types
attachments = [
    "RBT", "LRBT", "LBT", "FRBT", "FLRBT", "FLBT",
    "FRT", "FLRT", "FLT", "RBTD", "LRBTD", "LBTD",
    "FRBTD", "FLRBTD", "FLBTD", "FRTD", "FLRTD", "FLTD",
    "RBD", "LRBD", "LBD", "FRBD", "FLRBD", "FLBD",
    "FRD", "FLRD", "FLD"
]

# Counter for the current CSV file number
file_count = 1
output_directory = r"C:\Masonry\New_A\Rooms"
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Maximum number of rows per CSV
max_rows_per_file = 400_000
row_count = 0

# Initialize a DataFrame for the current CSV file
current_df = []

# Generate room dimensions for each combination of length, width, height, attachment, inner wall, and outer wall
for length in lengths:
    for width in widths:
        for height in heights:
            for inner_wall in inner_wall_widths:
                for outer_wall in outer_wall_widths:
                    for attachment in attachments:
                        # Append the room dimension
                        current_df.append([length, width, height, inner_wall, outer_wall, attachment])
                        row_count += 1
                        
                        # Check if the current DataFrame has reached the maximum number of rows
                        if row_count >= max_rows_per_file:
                            # Create a DataFrame from the collected dimensions
                            df = pd.DataFrame(current_df, columns=['Length', 'Width', 'Height', 'Inner Wall Width', 'Outer Wall Width', 'Attachment'])
                            
                            # Add a 'Number' column
                            df['Number'] = range(1, len(df) + 1)
                            
                            # Save to CSV file
                            output_file_path = os.path.join(output_directory, f'room_dimensions_{file_count}.csv')
                            df.to_csv(output_file_path, index=False)
                            
                            print(f"Room dimensions CSV file created successfully at: {output_file_path}")
                            
                            # Reset for the next file
                            current_df = []
                            row_count = 0
                            file_count += 1

# Save any remaining entries to a final CSV file if there are any
if current_df:
    df = pd.DataFrame(current_df, columns=['Length', 'Width', 'Height', 'Inner Wall Width', 'Outer Wall Width', 'Attachment'])
    df['Number'] = range(1, len(df) + 1)
    output_file_path = os.path.join(output_directory, f'room_dimensions_{file_count}.csv')
    df.to_csv(output_file_path, index=False)
    print(f"Room dimensions CSV file created successfully at: {output_file_path}")
