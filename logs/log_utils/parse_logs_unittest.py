import unittest
from datetime import datetime
import parse_logs

# Assuming Log is a class representing the log entries with attributes severity, payload, and timestamp.
class Log:
    def __init__(self, severity, payload, timestamp):
        self.severity = severity
        self.payload = payload
        self.timestamp = timestamp

class TestLogExtractor(unittest.TestCase):
    def test_extract_logs_between_markers(self):
        # Prepare sample logs for testing
        logs = [
            # Sample log entries that mimic your log format
            Log(None, "=== START LOG ===", datetime.now()),
            Log(None, "Benchmark passed", datetime.now()),
            Log(None, "TaskId: 123", datetime.now()),
            Log(None, "Time: 10.5", datetime.now()),
            Log(None, "Retries: 1", datetime.now()),
            Log(None, "=== END LOG ===", datetime.now()),
            Log("DEBUG", "Function execution took 8 ms, finished with status code: 200", datetime.now()),

            Log(None, "=== START LOG ===", datetime.now()),
            Log(None, "Benchmark passed", datetime.now()),
            Log(None, "TaskId: 321", datetime.now()),
            Log(None, "Time: 0.512", datetime.now()),
            Log(None, "Retries: 0", datetime.now()),
            Log(None, "=== END LOG ===", datetime.now()),
            Log("DEBUG", "Function execution took 9 ms, finished with status code: 200", datetime.now()),

            Log(None, "=== START LOG ===", datetime.now()),
            Log(None, "Max retries reached", datetime.now()),
            Log(None, "TaskId: 456", datetime.now()),
            Log(None, "Time: 30.7", datetime.now()),
            Log(None, "Retries: 3", datetime.now()),
            Log(None, "=== END LOG ===", datetime.now()),
            Log("DEBUG", "Function execution took 10 ms, finished with status code: 200", datetime.now()),
        ]
        expected_output = [
            # Expected output for the sample logs
            {
            "count": 0,
            "timestamp": logs[6].timestamp.isoformat(),
            "log": "Benchmark passed",
            "taskid": "123",
            "totalbenchmarktime": 10.5,
            "retries": 1,
            "functionexectime": 8.0,
        },
        {
            "count": 1,
            "timestamp": logs[13].timestamp.isoformat(),
            "log": "Benchmark passed",
            "taskid": "321",
            "totalbenchmarktime": 0.512,
            "retries": 0,
            "functionexectime": 9.0,
        },
        {
            "count": 2,
            "timestamp": logs[20].timestamp.isoformat(),
            "log": "Max retries reached",
            "taskid": "456",
            "totalbenchmarktime": 30.7,
            "retries": 3,
            "functionexectime": 10.0,
        }
        ]
        result = parse_logs.parse_between_markers(logs)
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()