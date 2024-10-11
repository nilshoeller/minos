import json
import csv
import os
from datetime import datetime

import google.cloud.logging # type: ignore
from google.cloud.logging import ASCENDING # type: ignore
# from google.cloud.logging import DESCENDING # type: ignore

from log_utils import parse_logs

def get_cloud_function_logs(function_name, project_id, limit=10):
    # Create a client to access Cloud Logging
    client = google.cloud.logging.Client(project=project_id)
    logger_filter = (
        f'resource.type="cloud_function" '
        f'resource.labels.function_name="{function_name}" '
        f'(severity:"DEFAULT" OR severity:"DEBUG")'
    )
    # Fetch logs
    entries = client.list_entries(filter_=logger_filter, order_by=ASCENDING, page_size=limit)

    # print("COUNT: ", len(list(entries)))
    print(f"Logs for Cloud Function: {function_name}\n")

    return parse_logs.parse_between_markers(entries)

def save_logs_to_csv(logs, folder_name='logs_archive'):
    # Create a folder to store the CSV file if it doesn't exist
    os.makedirs(folder_name, exist_ok=True)
    
    # Get the current date for the file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f'cloud_function_logs_{current_date}.csv'  # Include the date in the file name


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

if __name__ == "__main__":
    # Replace with your Cloud Function name and Google Cloud project ID
    function_name = "optimizationFunction"
    project_id = "bsc-thesis-implementation"

    # Fetch and print logs
    logs = get_cloud_function_logs(function_name, project_id, limit=100)

    # # Print logs and return them as JSON
    # print(json.dumps(logs, indent=2))  # Pretty print JSON

    # Save logs to CSV
    save_logs_to_csv(logs)