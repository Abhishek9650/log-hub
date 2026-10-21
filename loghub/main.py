import re
import json

def read_logs(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        logs = file.readlines()
    return logs

def parse_log(logs):
    pattern = r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)"

    match = re.match(pattern, logs.strip())

    if match:
        return match.groups()

    return None


def json_parse_log(logs):
    try:
        return json.loads(logs)
    except json.JSONDecodeError:
        return None

def log_to_dict(parts):
    if parts is None or len(parts) < 4:
        return None

    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2],
        "message": parts[3]
    }


def process_logs(logs):
    results = []
    invalid_logs = []

    for log in logs:
        if not log.strip():
            continue

        if log.strip().startswith("{"):
            parsed_log = json_parse_log(log)

            if parsed_log is None:
                invalid_logs.append({
                    "raw": log.strip(),
                    "reason": "invalid_json"
                })
                continue

            # Normalize JSON fields to the same output structure.
            if not all(key in parsed_log for key in
                       ("timestamp", "level", "message")):
                invalid_logs.append({
                    "raw": log.strip(),
                    "reason": "missing_required_json_fields"
                })
                continue

        else:
            parts = parse_log(log)

            if parts is None:
                invalid_logs.append({
                    "raw": log.strip(),
                    "reason": "unsupported_text_format"
                })
                continue

            parsed_log = log_to_dict(parts)

            if parsed_log is None:
                invalid_logs.append({
                    "raw": log.strip(),
                    "reason": "invalid_text_format"
                })
                continue

        results.append(parsed_log)

    return results, invalid_logs


if __name__ == "__main__":
    logs = read_logs("data/sample_logs.log")
    results, invalid_logs = process_logs(logs)

    print("Valid logs:")
    print(results)

    print("\nInvalid logs:")
    print(invalid_logs)
