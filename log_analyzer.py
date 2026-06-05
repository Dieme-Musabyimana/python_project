import sys

file_name = sys.argv[1]

#Read file
file = open(file_name)
errors = 0
inf = 0
warnings = 0
error_count = { }

for line in file:
    print(line.strip())
    part = line.strip().split()
    time_stamp = part[0] + " " + part[1]
    level = part[2]
    message = " ".join(part[3:])
    print("time stamp: " + time_stamp)
    print("level: " + level)
    print("message: " + message)


    if level == "ERROR":
        errors+=1
        if message not in error_count:
            error_count[message]=1
        else: error_count[message]+=1
    elif level == "INFO":
        inf+=1
    elif level == "WARNING":
        warnings+=1

print(f"ERRORS: {errors}")
print(f"INF: {inf}")
print(f"WARNING: {warnings}")
print("Most frequent error:", max(error_count, key=error_count.get))
file.close()