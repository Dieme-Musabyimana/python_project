import sys
import json

file_name = sys.argv[1]

# Filters declaration
filter_level = None
filter_from = None
filter_to = None
export_file = None

# Filters logic
i = 2
while i < len(sys.argv):
    if sys.argv[i] == "--level":
        filter_level = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == "--from":
        filter_from = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == "--to":
        filter_to = sys.argv[i + 1]
        i += 2
    elif sys.argv[i] == "--export":
        export_file = sys.argv[i + 1]
        i += 2
    else:
        i += 1

# Counters
errors = 0
inf = 0
warnings = 0
error_count = {}
failure_timestamps = []
total_logs = 0


with open(file_name, "r") as file:
    for line in file:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue

        # Feature-2: Detect and parse format
        try:
            # Try parsing as JSON first
            log_data = json.loads(cleaned_line)
            time_stamp = log_data.get("timestamp", "")
            level = log_data.get("level", "").strip()
            message = log_data.get("message", "")
        except json.JSONDecodeError:
            #Try plain text parsing if JSON parsing fails
            part = cleaned_line.split()
            if len(part) < 4:
                continue
            time_stamp = part[0] + " " + part[1]
            level = part[2].strip()
            message = " ".join(part[3:])

        # Feature-5: Apply filter logic based on parsed fields
        if filter_level is not None and level != filter_level:
            continue

        if filter_from is not None and time_stamp < filter_from:
            continue

        if filter_to is not None and time_stamp > filter_to:
            continue

        total_logs += 1

        # Feature-3: Count log levels
        if level == "ERROR":
            errors += 1
            # Feature-4: Track error message frequencies
            if message not in error_count:
                error_count[message] = 1
            else:
                error_count[message] += 1

            # Extract time segment from timestamp for final output tracking
            time_parts = time_stamp.split()
            time_only = time_parts[1] if len(time_parts) > 1 else time_stamp
            failure_timestamps.append(time_only)

        elif level == "INFO":
            inf += 1
        elif level == "WARNING":
            warnings += 1

# Find most common error
most_common_error = "None"
if error_count:
    most_common_error = max(error_count, key=error_count.get)

# Final Output Specification Format
print(f"Total logs:           {total_logs}")
print(f"Errors:                 {errors}")
print(f"Warnings:              {warnings}")
print(f"Info:                 {inf}")
if error_count:
    print(f'Most frequent error:  "{most_common_error}"')
else:
    print('Most frequent error:  "None"')
print(f"Failure timestamps:   {', '.join(failure_timestamps)}")

# Feature-6 & Reviewer Comment: Export to CSV using a Context Manager
if export_file is not None:
    with open(export_file, "w") as f:
        f.write("metric,value\n")
        f.write(f"total_logs,{total_logs}\n")
        f.write(f"errors,{errors}\n")
        f.write(f"warnings,{warnings}\n")
        f.write(f"info,{inf}\n")
        f.write(f"most_common_error,{most_common_error}\n")

    print("\nCSV exported to:", export_file)