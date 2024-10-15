import os
import csv
from datetime import datetime


def save_to_csv(function_name, logs, folder_name='logs_archive'):
    # Create a folder to store the CSV file if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Get the current date for the file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f'{current_date}-{function_name}-logs.csv'  # Include the date in the file name

    # Define the full path for the CSV file
    csv_file_path = os.path.join(folder_name, file_name)

    # Get the keys for the CSV header from the first log entry
    if logs:
        header = logs[0].keys()  # Assumes all log entries have the same structure

        # Write logs to a CSV file
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            writer.writerows(logs)

        print(f"Logs saved to {csv_file_path}")
    else:
        print("No logs to save.")