import pandas as pd
import numpy as np
import os

# Initialize an empty list to store room dimensions
room_dimensions = []

# Define the attachment types
attachments = [
    "RBT", "LRBT", "LBT", "FRBT", "FLRBT", "FLBT",
    "FRT", "FLRT", "FLT", "RBTD", "LRBTD", "LBTD",
    "FRBTD", "FLRBTD", "FLBTD", "FRTD", "FLRTD", "FLTD",
    "RBD", "LRBD", "LBD", "FRBD", "FLRBD", "FLBD",
    "FRD", "FLRD", "FLD"
]

# Generate lengths, widths, and heights from 10 to 40 in increments of 2.5
lengths = np.arange(10, 42.5, 2.5)  # Lengths from 10 to 40
widths = np.arange(10, 42.5, 2.5)   # Widths from 10 to 40
heights = np.arange(10, 42.5, 2.5)  # Heights from 10 to 40

# Counter for the current CSV file number
file_count = 1
output_directory = r"C:\Masonry\New_A\Rooms"
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Maximum number of rows per CSV
max_rows_per_file = 400_000
row_count = 0

# Initialize a DataFrame for the current CSV file
current_df = []

# Generate room dimensions for each combination of length, width, height, and attachment
for length in lengths:
    for width in widths:
        for height in heights:
            for attachment in attachments:
                # Append the room dimension
                current_df.append([length, width, height, attachment])
                row_count += 1
                
                # Check if the current DataFrame has reached the maximum number of rows
                if row_count >= max_rows_per_file:
                    # Create a DataFrame from the collected dimensions
                    df = pd.DataFrame(current_df, columns=['Length', 'Width', 'Height', 'Attachment'])
                    
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
    df = pd.DataFrame(current_df, columns=['Length', 'Width', 'Height', 'Attachment'])
    df['Number'] = range(1, len(df) + 1)
    output_file_path = os.path.join(output_directory, f'room_dimensions_{file_count}.csv')
    df.to_csv(output_file_path, index=False)
    print(f"Room dimensions CSV file created successfully at: {output_file_path}")
