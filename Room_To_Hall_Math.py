import csv
import os
import itertools

# Define the numbers to add
numbers = [36, 48, 60, 72, 84, 96]

# Initialize a list to store the results
results = []

# Generate permutations of all lengths from 1 to 6
for r in range(1, len(numbers) + 1):  # From 1 to 6
    # Generate permutations
    for permutation in itertools.product(numbers, repeat=r):
        # Create a row with zeros followed by the permutation
        row = [0] * (6 - len(permutation)) + list(permutation)
        # Calculate the total by summing all cells in the row
        total = sum(row)
        row.append(total)  # Append the total to the row
        # Append the row to results
        results.append(row)

# Define the output file path
output_file = r"C:\Masonry\permutations_results.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write the results to a CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(results)

print(f"Results saved to {output_file}")
