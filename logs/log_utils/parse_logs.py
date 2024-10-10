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
        "time": None,
        "retries": None,
    }

    for log in logs:
        # print-statements in google cloud functions are marked with DEFAULT/None in the LOGS
        if log.severity == None:    
            if log.payload == start_marker:
                is_between_markers = True
                new_log["count"] = count
                new_log["timestamp"] = log.timestamp.isoformat()
                continue
            
            if log.payload == end_marker:
                is_between_markers = False
                relevant_logs.append(new_log)
                count += 1
                new_log = {
                    "count": None,
                    "timestamp": None,
                    "log": None,
                    "taskid": None,
                    "time": None,
                    "retries": None,
                    }
                continue
            
            if is_between_markers:
                if "Benchmark" in log.payload or "Max" in log.payload:
                    new_log["log"] = log.payload
                    continue
                if "TaskId" in log.payload:
                    new_log["taskid"] = log.payload.replace("TaskId: ", "")
                    continue
                if "Time" in log.payload:
                    new_log["time"] = float(log.payload.replace("Time: ", ""))
                    continue
                if "Retries" in log.payload:
                    new_log["retries"] = int(log.payload.replace("Retries: ", ""))
                    continue
            
    return relevant_logs