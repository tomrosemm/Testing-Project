import csv

def calculate_average(csv_file_path: str) -> float:
    total = 0
    count = 0

    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) > 1:  # Ensure the row has at least two columns
                try:
                    total += float(row[1])
                    count += 1
                except ValueError:
                    pass  # Skip rows where the second column isn't a number

    if count == 0:
        raise ValueError("No valid numerical data found in the second column.")

    return total / count

# Example usage
csv_file_path = 'Testing-Project/toqito.git_file_changes.csv'
average = calculate_average(csv_file_path)
print(f"The average of the second column is: {average}")