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

def get_cloud_function_logs(function_type: CloudFunction, project_id: str, exec_minutes: int):
    # Create a client to access Cloud Logging
    client = logging.Client(project=project_id)

    # construct a date object representing yesterday
    # timestamp_limit = datetime.now(timezone.utc) - timedelta(days=1)
    timestamp_limit = datetime.now(timezone.utc) - timedelta(minutes=exec_minutes)
    # Cloud Logging expects a timestamp in RFC3339 UTC "Zulu" format
    # https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    logger_filter = (
        f'resource.type="cloud_function" '
        f'AND resource.labels.function_name="{function_type.value}" '
        f'AND (severity:"DEFAULT" OR severity:"DEBUG") '
        f'AND timestamp>="{timestamp_limit.strftime(time_format)}"'
    )
    # Fetch logs
    entries = client.list_entries(filter_=logger_filter, order_by=ASCENDING)
    # print("COUNT: ", len(list(entries)))

    print(f"Logs for Cloud Function: {function_type.value}\n")
    if function_type == CloudFunction.OPTIMIZED:
        return parse_logs.parse_optimized_func(entries)
    if function_type == CloudFunction.BASELINE:
        return parse_logs.parse_baseline_func(entries)
    
    return []

def fetch_logs_and_save(function_type: CloudFunction, project_id: str, minutes: int):
    fetched_list = get_cloud_function_logs(function_type, project_id, minutes)
    csv_log_saver.save_to_csv(function_type.value, fetched_list)

def fetch_logs_and_save_both(minutes: int):
    fetched_list = get_cloud_function_logs(CloudFunction.OPTIMIZED, PROJECT_ID, minutes)
    csv_log_saver.save_to_csv(CloudFunction.OPTIMIZED.value, fetched_list)

    fetched_list = get_cloud_function_logs(CloudFunction.BASELINE, PROJECT_ID, minutes)
    csv_log_saver.save_to_csv(CloudFunction.BASELINE.value, fetched_list)