import re

def parse_between_markers(logs):
    start_marker = "=== START LOG ==="
    end_marker = "=== END LOG ==="
    
    # Variables to hold the result and state of parsing
    is_between_markers = False
    relevant_logs = []
    count = 0  # Initialize count

    new_log = {
        "count": None,
        "timestamp": None,
        "log": None,
        "taskid": None,
        "totalbenchmarktime": None,
        "retries": None,
        "functionexectime": None,
    }

    for log in logs:
        # print(f"severity: {log.severity} - log: {log.payload}")
        # print-statements in google cloud functions are marked with DEFAULT/None in the LOGS
        if log.severity == None:    
            if log.payload == start_marker:
                is_between_markers = True
                continue
            
            if log.payload == end_marker:
                is_between_markers = False
                continue
            
            if is_between_markers:
                if "Benchmark" in log.payload or "Max" in log.payload:
                    new_log["log"] = log.payload
                    continue
                if "TaskId" in log.payload:
                    new_log["taskid"] = log.payload.replace("TaskId: ", "")
                    continue
                if "Time" in log.payload:
                    new_log["totalbenchmarktime"] = float(log.payload.replace("Time: ", ""))
                    continue
                if "Retries" in log.payload:
                    new_log["retries"] = int(log.payload.replace("Retries: ", ""))
                    continue
        
        if log.severity == "DEBUG" and "Function execution took" in log.payload:
            # print(f"severity: {log.severity} - log: {log.payload}")
            
            new_log["count"] = count
            new_log["timestamp"] = log.timestamp.isoformat()
            new_log["functionexectime"] = extract_execution_time(log.payload)
            
            relevant_logs.append(new_log)
            count += 1
            new_log = {
                "count": None,
                "timestamp": None,
                "log": None,
                "taskid": None,
                "totalbenchmarktime": None,
                "retries": None,
                "functionexectime": None,
                }
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