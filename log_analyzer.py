import sys

file_name = sys.argv[1]

#filters declaration
filter_level = None
filter_from = None
filter_to = None
export_file = None

#filters logic
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

file = open(file_name)

#counters
errors = 0
inf = 0
warnings = 0
error_count = {}
most_common_error = 0
total_logs = 0

#loop through lines to read them
for line in file:
    part = line.strip().split()

    #extract log parts
    time_stamp = part[0] + " " + part[1]
    level = part[2]
    message = " ".join(part[3:])

    #apply filters
    if filter_level is not None:
        if level != filter_level:
            continue

    if filter_from is not None:
        if time_stamp < filter_from:
            continue

    if filter_to is not None:
        if time_stamp > filter_to:
            continue

    total_logs += 1

    #print logs
    print(line.strip())
    print("time stamp: " + time_stamp)
    print("level: " + level)
    print("message: " + message)

    #count levels
    if level == "ERROR":
        errors += 1

        if message not in error_count:
            error_count[message] = 1
        else:
            error_count[message] += 1

    elif level == "INFO":
        inf += 1

    elif level == "WARNING":
        warnings += 1

file.close()

#final summary
print(f"ERRORS: {errors}")
print(f"INF: {inf}")
print(f"WARNING: {warnings}")

#find most common error
if error_count:
    most_common_error = max(error_count, key=error_count.get)
    print("Most frequent error:", most_common_error)

#export to CSV
if export_file is not None:
    f = open(export_file, "w")

    f.write("metric,value\n")
    f.write(f"total_logs,{total_logs}\n")
    f.write(f"errors,{errors}\n")
    f.write(f"warnings,{warnings}\n")
    f.write(f"info,{inf}\n")
    f.write(f"most_common_error,{most_common_error}\n")

    f.close()

    print("\nCSV exported to:", export_file)