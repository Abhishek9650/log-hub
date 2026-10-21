









def read_logs(file_path):
    with open(file_path, "r", encoding="utf-8") as file: #encoding="utf-8" supports common text characters. #as file gives us a variable through which we can access the opened file.
        logs = file.readlines()
        return logs
        
        pass #The indented pass is still temporary.

def parse_log(logs):
    parts = logs.strip().split(" ",3)
    return parts

def log_to_dict(parts):
    log = { "timestamp" : f"{parts[0]}  {parts[1]}" ,
            "level" : parts[2],
            "message" : parts[3]
            }
    return  log

def process_logs(logs):
    results = []
    for log in logs:
        parts = parse_log(log)
        parse_log = log_to_dict(parts)
        results.append(parse_log)
    return results


if __name__ == "__main__":  #It means: execute this block only when the Python file is run directly, not when it is imported into another Python file.
    logs = read_logs("data/sample_logs.log")
    results = process_logs(logs)
    print(results)