import re
log = "2026-10-17 10:00:15 ERROR Database connection timeout"

pattern = r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)"

match = re.match(pattern, log)

if match:
    print(match.groups())

def read_logs(file_path):
    with open(file_path, "r", encoding="utf-8") as file: #encoding="utf-8" supports common text characters. #as file gives us a variable through which we can access the opened file.
        logs = file.readlines()
        return logs
        
        pass #The indented pass is still temporary.

def parse_log(logs):
    parts = logs.strip().split(" ",3)
    return parts

def json_parse_log(logs):
    import json
    try:
        return json.loads(logs)
    except json.JSONDecodeError:
        return None

def log_to_dict(parts):
    if len(parts) < 4 :
        return None
    log = { "timestamp" : f"{parts[0]} {parts[1]}" ,
            "level" : parts[2],
            "message" : parts[3]
            }
    return  log

def process_logs(logs):
    results = []
    invalid_logs =[]
    for log in logs:

        if log.strip().startswith("{"):
            #json = True
            parsed_log= json_parse_log(log)

            if parsed_log is None:
                invalid_logs.append({
                "raw": log.strip(),
                "reason": "invalid_json"
                })
                continue
            
        else :
            #Space_seperated = True
            parts= parse_log(log)
            parsed_log = log_to_dict(parts)
            if parsed_log is None:
                invalid_logs.append({
                "raw": log.strip(),
                "reason": "invalid_text_format"
                })
                continue

        results.append(parsed_log)
    return results,invalid_logs


if __name__ == "__main__":  #It means: execute this block only when the Python file is run directly, not when it is imported into another Python file.
    logs = read_logs("data/sample_logs.log")
    results,invalid_logs = process_logs(logs)
    print(results)
    print(invalid_logs)