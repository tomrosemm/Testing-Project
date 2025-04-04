import csv
import pandas as pd

def filter_csv(input_file, output_file, columns_to_keep):
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    
    except pd.errors.EmptyDataError:
        print("Error: The input file is empty.")
        return

    filtered_df = df[[col for col in columns_to_keep if col in df.columns]]

    filtered_df.to_csv(output_file, index=False)
    print(f"Filtered CSV saved to '{output_file}' successfully.")

if __name__ == "__main__":

    input_file = "input.csv"
    output_file = "filtered_output.csv"
    columns_to_keep = ["Name", "Age", "Email"]

    filter_csv(input_file, output_file, columns_to_keep)