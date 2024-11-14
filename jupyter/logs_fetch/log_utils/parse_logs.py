import re

START_MARKER = "Function execution started"
END_MARKER_DURATION = "Function execution took"
    
START_MARKER_LOG = "=== START LOG ==="
END_MARKER_LOG = "=== END LOG ==="

EXECUTION_FINISHED_MARKER = "Execution finished"
MAX_RETRIES_MARKER = "Max retries reached"

BENCHMARK_DURATION = "Benchmark-duration"
DOWNLOAD_DURATION = "Download-duration"
FAST_INSTANCE = "Fast instance"

CRASHING_INSTANCE = "Crashing instance"

microsecond_symbol = "µs"
millisecond_symbol = "ms"

def parse_func_logs(logs) -> list:
    # Dictionary to store logs grouped by execution_id
    grouped_logs = {}
    count = 0

    for log in logs:
        execution_id = log.labels.get('execution_id')

        if execution_id not in grouped_logs:
            grouped_logs[execution_id] = {
                "count": count,
                "timestamp": None,
                "execution_id": execution_id,
                "log": None,
                "retries": 0,
                "execution_time": None,
                "benchmark_duration": None,
                "download_duration": "---",
            }
            count += 1

        current_log = grouped_logs[execution_id]
        
        if log.severity == "DEBUG" and START_MARKER in log.payload:
            continue

        if log.severity is None:
            if log.payload == START_MARKER_LOG:
                continue
            if log.payload == END_MARKER_LOG:
                continue
            if EXECUTION_FINISHED_MARKER in log.payload or MAX_RETRIES_MARKER in log.payload:
                current_log["log"] = log.payload
                continue
            if "TaskId" in log.payload:
                # current_log["taskid"] = log.payload.replace("TaskId: ", "")
                continue
            if "Retries" in log.payload:
                current_log["retries"] = int(log.payload.replace("Retries: ", ""))
                continue
            if BENCHMARK_DURATION in log.payload:
                current_log["benchmark_duration"] = log.payload.replace("Benchmark-duration: ", "") + " " + microsecond_symbol
                continue
            if FAST_INSTANCE in log.payload:
                current_log["download_duration"] = log.payload
                continue
            if DOWNLOAD_DURATION in log.payload:
                current_log["download_duration"] = log.payload.replace("Download-duration: ", "") + " " + millisecond_symbol
                continue
            if CRASHING_INSTANCE in log.payload:
                current_log["log"] = log.payload
                continue

        if log.severity == "DEBUG" and END_MARKER_DURATION in log.payload:
            current_log["timestamp"] = log.timestamp.isoformat()
            current_log["execution_time"] = extract_execution_time(log.payload)

    # Convert dictionary to list of logs
    relevant_logs = list(grouped_logs.values())
    return relevant_logs

def extract_execution_time(log_string):
    # Use a regular expression to find the time in milliseconds
    match = re.search(r"Function execution took (\d+\.?\d*) ms", log_string)
    
    if match:
        # Convert the matched time to a float
        execution_time = float(match.group(1))
        return execution_time
    else:
        return None