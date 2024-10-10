import json
import google.cloud.logging # type: ignore
from google.cloud.logging import ASCENDING # type: ignore
# from google.cloud.logging import DESCENDING # type: ignore
from log_utils import parse_logs

# def parse_logs_between_markers(logs):
#     start_marker = "=== START LOG ==="
#     end_marker = "=== END LOG ==="
    
#     # Variables to hold the result and state of parsing
#     is_between_markers = False
#     relevant_logs = []
#     count = 0  # Initialize count

#     new_log = {
#         "count": None,
#         "timestamp": None,
#         "log": None,
#         "taskid": None,
#         "time": None,
#         "retries": None,
#     }

#     for log in logs:
#         # print-statements in google cloud functions are marked with DEFAULT/None in the LOGS
#         if log.severity == None:    
#             if log.payload == start_marker:
#                 is_between_markers = True
#                 new_log["count"] = count
#                 new_log["timestamp"] = log.timestamp.isoformat()
#                 continue
            
#             if log.payload == end_marker:
#                 is_between_markers = False
#                 relevant_logs.append(new_log)
#                 count += 1
#                 new_log = {
#                     "count": None,
#                     "timestamp": None,
#                     "log": None,
#                     "taskid": None,
#                     "time": None,
#                     "retries": None,
#                     }
#                 continue
            
#             if is_between_markers:
#                 if "Benchmark" in log.payload or "Max" in log.payload:
#                     new_log["log"] = log.payload
#                     continue
#                 if "TaskId" in log.payload:
#                     new_log["taskid"] = log.payload.replace("TaskId: ", "")
#                     continue
#                 if "Time" in log.payload:
#                     new_log["time"] = float(log.payload.replace("Time: ", ""))
#                     continue
#                 if "Retries" in log.payload:
#                     new_log["retries"] = int(log.payload.replace("Retries: ", ""))
#                     continue
            
#     return relevant_logs

def get_cloud_function_logs(function_name, project_id, limit=10):
    # Create a client to access Cloud Logging
    client = google.cloud.logging.Client(project=project_id)
    # Set up the logger filter to retrieve logs only for your Cloud Function
    logger_filter = (
        f'resource.type="cloud_function" '
        f'resource.labels.function_name="{function_name}" '
        f'severity:"DEFAULT"'
    )
    # Fetch logs
    entries = client.list_entries(filter_=logger_filter, order_by=ASCENDING, page_size=limit)

    # print("COUNT: ", len(list(entries)))
    print(f"Logs for Cloud Function: {function_name}\n")

    return parse_logs.parse_between_markers(entries)

if __name__ == "__main__":
    # Replace with your Cloud Function name and Google Cloud project ID
    function_name = "optimizationFunction"
    project_id = "bsc-thesis-implementation"

    # Fetch and print logs
    logs = get_cloud_function_logs(function_name, project_id, limit=100)

    # Print logs and return them as JSON
    print(json.dumps(logs, indent=2))  # Pretty print JSON