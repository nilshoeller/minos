import re

def parse_optimized_func(logs):

    start_marker = "Function execution started"
    end_marker_duration = "Function execution took"
    
    start_marker_log = "=== START LOG ==="
    end_marker_log = "=== END LOG ==="

    # Variables to hold the result and state of parsing
    is_between_markers = False
    is_other_end_marker_parsed = False

    relevant_logs = []
    count = 0  # Initialize count

    new_log = None

    for log in logs:
        # print(f"severity: {log.severity} - log: {log.payload}")

        if log.severity == "DEBUG" and start_marker in log.payload:
            new_log = {
                "count": None,
                "timestamp": None,
                "log": None,
                "taskid": None,
                "retries": None,
                "functionexectime": None,
                }
            count += 1
            continue

        # PRINTS in gcp-function-logs are marked with DEFAULT (in gcp) and None (in pyhton)
        if log.severity == None:    
            if log.payload == start_marker_log:
                is_between_markers = True
                continue
            
            if log.payload == end_marker_log:
                is_between_markers = False
                if is_other_end_marker_parsed:
                    relevant_logs.append(new_log)
                    is_other_end_marker_parsed = False
                else:
                    is_other_end_marker_parsed = True
                continue
            
            if is_between_markers:
                if "Benchmark" in log.payload or "Max" in log.payload:
                    new_log["log"] = log.payload
                    continue
                if "TaskId" in log.payload:
                    new_log["taskid"] = log.payload.replace("TaskId: ", "")
                    continue
                if "Retries" in log.payload:
                    new_log["retries"] = int(log.payload.replace("Retries: ", ""))
                    continue
        
        if log.severity == "DEBUG" and end_marker_duration in log.payload:
            new_log["count"] = count
            new_log["timestamp"] = log.timestamp.isoformat()
            new_log["functionexectime"] = extract_execution_time(log.payload)

            if is_other_end_marker_parsed:
                relevant_logs.append(new_log)
                is_other_end_marker_parsed = False
            else:
                is_other_end_marker_parsed = True    

    return relevant_logs


def parse_baseline_func(logs):

    start_marker = "Function execution started"
    end_marker_duration = "Function execution took"
    
    start_marker_log = "=== START LOG ==="
    end_marker_log = "=== END LOG ==="

    # Variables to hold the result and state of parsing
    is_between_markers = False
    is_other_end_marker_parsed = False

    relevant_logs = []
    count = 0  # Initialize count

    new_log = None

    for log in logs:
        # print(f"severity: {log.severity} - log: {log.payload}")

        if log.severity == "DEBUG" and start_marker in log.payload:
            new_log = {
                "count": None,
                "timestamp": None,
                "log": None,
                "taskid": None,
                "functionexectime": None,
                }
            count += 1
            continue

        # PRINTS in gcp-function-logs are marked with DEFAULT (in gcp) and None (in pyhton)
        if log.severity == None:    
            if log.payload == start_marker_log:
                is_between_markers = True
                continue
            
            if log.payload == end_marker_log:
                is_between_markers = False
                if is_other_end_marker_parsed:
                    relevant_logs.append(new_log)
                    is_other_end_marker_parsed = False
                else:
                    is_other_end_marker_parsed = True
                continue
            
            if is_between_markers:
                if "Execution finished." in log.payload:
                    new_log["log"] = log.payload
                    continue
                if "TaskId" in log.payload:
                    new_log["taskid"] = log.payload.replace("TaskId: ", "")
                    continue
        
        if log.severity == "DEBUG" and end_marker_duration in log.payload:
            new_log["count"] = count
            new_log["timestamp"] = log.timestamp.isoformat()
            new_log["functionexectime"] = extract_execution_time(log.payload)

            if is_other_end_marker_parsed:
                relevant_logs.append(new_log)
                is_other_end_marker_parsed = False
            else:
                is_other_end_marker_parsed = True    

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