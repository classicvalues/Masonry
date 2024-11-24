import pandas as pd
import os

# Define the output directory
output_directory = r"C:\Masonry\ALL_A\ROOMS"
os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize an empty list to store item dimensions
item_dimensions = []

# Define the maximum dimension (0.0984252 feet)
max_dimension = 0.0984252

# Define how many rows per CSV file
rows_per_file = 400000
file_count = 1
current_row_count = 0

# Define the attachments
attachments = [
    "RBT", "LRBT", "LBT", "FRBT", "FLRBT", "FLBT", "FRT", "FLRT", "FLT",
    "RBTD", "LRBTD", "LBTD", "FRBTD", "FLRBTD", "FLBTD", "FRTD", "FLRTD", "FLTD",
    "RBD", "LRBD", "LBD", "FRBD", "FLRBD", "FLBD", "FRD", "FLRD", "FLD"
]

# Define the increment in feet (0.000328084 feet)
increment = 0.000328084

# Initialize the number for the Number column
number = 0.000000001000

# Generate dimensions from 0.000328084 to 0.0984252 in increments of 0.000328084
length = 0.000328084
while length <= max_dimension + 1e-9:  # Ensuring we include max_dimension with a tolerance
    width = 0.000328084
    while width <= max_dimension + 1e-9:
        height = 0.000328084
        while height <= max_dimension + 1e-9:
            for attachment in attachments:
                # Append item dimensions ensuring consistent formatting
                item_dimensions.append([
                    f"{length:.15f}",  # Length with 15 decimal places
                    f"{width:.15f}",   # Width with 15 decimal places
                    f"{height:.15f}",  # Height with 15 decimal places
                    attachment,
                    f"{number:.15f}"   # Number with 15 decimal places
                ])
                current_row_count += 1
                number = round(number + 0.000000001000, 15)  # Increment the number and round to 15 decimal places
                
                # Check if we've reached the limit for the current file
                if current_row_count >= rows_per_file:
                    # Create a DataFrame from the item dimensions
                    df = pd.DataFrame(item_dimensions, columns=['Length (ft)', 'Width (ft)', 'Height (ft)', 'Attachment', 'Number'])
                    
                    # Save to CSV file, explicitly setting the float format
                    output_file_path = os.path.join(output_directory, f'home_items_{file_count}.csv')
                    df.to_csv(output_file_path, index=False)
                    
                    print(f"Home items CSV file {file_count} created successfully at: {output_file_path}")
                    
                    # Reset for the next file
                    item_dimensions = []
                    current_row_count = 0
                    file_count += 1
            
            height = round(height + increment, 15)  # Round height to maintain precision
        width = round(width + increment, 15)  # Round width to maintain precision
    length = round(length + increment, 15)  # Round length to maintain precision

# Handle remaining items after the last full file
if item_dimensions:
    df = pd.DataFrame(item_dimensions, columns=['Length (ft)', 'Width (ft)', 'Height (ft)', 'Attachment', 'Number'])
    output_file_path = os.path.join(output_directory, f'home_items_{file_count}.csv')
    df.to_csv(output_file_path, index=False)
    print(f"Home items CSV file {file_count} created successfully at: {output_file_path}")
