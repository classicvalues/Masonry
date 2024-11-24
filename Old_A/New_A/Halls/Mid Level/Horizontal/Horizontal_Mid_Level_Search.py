import pandas as pd
import os

# Define the input and output file paths
input_file_path = r"C:\Masonry\New_A\Rooms\room_dimensions_1.csv"
output_directory = r"C:\Masonry\New_A\Halls\Mid Level\Horizontal"  # Updated output path
output_file_path = os.path.join(output_directory, 'filtered_rooms.csv')

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Read the CSV file
df = pd.read_csv(input_file_path)

# Filter conditions
length_condition = (df['Length'] >= 36) & (df['Length'] <= 72) & ((df['Length'] - 36) % 12 == 0)
width_condition = (df['Width'] >= 72) & (df['Width'] <= 576) & ((df['Width'] - 72) % 12 == 0)
inner_wall_condition = (df['Inner Wall Width'] >= 1.0) & (df['Inner Wall Width'] <= 2.0)
outer_wall_condition = (df['Outer Wall Width'] >= 2.0) & (df['Outer Wall Width'] <= 4.0)

# Ensure outer wall widths are double the inner wall widths
outer_wall_double_inner = df['Outer Wall Width'] == 2 * df['Inner Wall Width']

# Combine conditions for attachment containing both 'T' and 'D' (case-sensitive)
attachment_condition = df['Attachment'].str.contains('T', na=False) & \
                      df['Attachment'].str.contains('D', na=False)

# Combine all conditions
final_condition = (length_condition & 
                   width_condition & 
                   inner_wall_condition & 
                   outer_wall_condition & 
                   outer_wall_double_inner & 
                   attachment_condition)

# Filter the DataFrame
filtered_rooms = df[final_condition]

# Select only the 'Number' column
result_numbers = filtered_rooms[['Number']]

# Save to a new CSV file
result_numbers.to_csv(output_file_path, index=False)

print(f"Filtered room numbers saved successfully to: {output_file_path}")
