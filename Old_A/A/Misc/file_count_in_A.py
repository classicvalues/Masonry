import os

def count_csv_files(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return 0

    # List all files in the directory and filter .csv files
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # Count the number of .csv files
    csv_count = len(csv_files)

    return csv_count

# Example usage
folder_path = r'/mnt/c/A/Halls'  # Use raw string to handle Windows file paths
csv_count = count_csv_files(folder_path)
print(f"There are {csv_count} .csv files in the folder {folder_path}.")
