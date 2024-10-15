import json
from datetime import datetime

import google.cloud.logging # type: ignore
from google.cloud.logging import ASCENDING # type: ignore
# from google.cloud.logging import DESCENDING # type: ignore

from log_utils import parse_logs
from log_utils import csv_log_saver

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

    return parse_logs.parse_optimized_func(entries)


if __name__ == "__main__":
    # Replace with your Cloud Function name and Google Cloud project ID
    function_name = "optimizedFunction"
    project_id = "bsc-thesis-implementation"

    # Fetch and print logs
    logs = get_cloud_function_logs(function_name, project_id, 100)

    # # Print logs and return them as JSON
    # print(json.dumps(logs, indent=2))  # Pretty print JSON

    # Save logs to CSV
    csv_log_saver.save_to_csv(function_name, logs)