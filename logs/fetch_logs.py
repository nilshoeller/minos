from google.cloud import logging # type: ignore
from google.cloud.logging import ASCENDING # type: ignore
# from google.cloud.logging import DESCENDING # type: ignore

from log_utils import parse_logs
from log_utils import csv_log_saver
from enum import Enum
from datetime import datetime, timedelta, timezone

PROJECT_ID = "bsc-thesis-implementation"

class CloudFunction(Enum):
    OPTIMIZED = "optimizedFunction"
    BASELINE = "baselineFunction"

def get_cloud_function_logs(function_type: CloudFunction, project_id: str, limit: int):
    # Create a client to access Cloud Logging
    client = logging.Client(project=project_id)

    # construct a date object representing yesterday
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    # yesterday = datetime.now(timezone.utc) - timedelta(minutes=5)
    
    # Cloud Logging expects a timestamp in RFC3339 UTC "Zulu" format
    # https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    logger_filter = (
        f'resource.type="cloud_function" '
        f'AND resource.labels.function_name="{function_type.value}" '
        f'AND (severity:"DEFAULT" OR severity:"DEBUG") '
        f'AND timestamp>="{yesterday.strftime(time_format)}"'
    )
    # Fetch logs
    entries = client.list_entries(filter_=logger_filter, order_by=ASCENDING, page_size=limit)
    # print("COUNT: ", len(list(entries)))

    print(f"Logs for Cloud Function: {function_type.value}\n")
    if function_type == CloudFunction.OPTIMIZED:
        return parse_logs.parse_optimized_func(entries)
    if function_type == CloudFunction.BASELINE:
        return parse_logs.parse_baseline_func(entries)
    
    return []


if __name__ == "__main__":
    # Fetch and print logs
    optimized_logs = get_cloud_function_logs(CloudFunction.OPTIMIZED, PROJECT_ID, 100)
    baseline_logs = get_cloud_function_logs(CloudFunction.BASELINE, PROJECT_ID, 100)
    
    # # Print logs and return them as JSON
    # print(json.dumps(optimized_logs, indent=2))  # Pretty print JSON

    # Save logs to CSV
    csv_log_saver.save_to_csv(CloudFunction.OPTIMIZED.value, optimized_logs)
    csv_log_saver.save_to_csv(CloudFunction.BASELINE.value, baseline_logs)