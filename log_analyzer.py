import sys

file_name = sys.argv[1]
file = open(file_name)

for line in file:
    print(line.strip())
    part = line.strip().split()
    time_stamp = part[0] + " " + part[1]
    level = part[2]
    message = part[3]
    print("time stamp: " + time_stamp)
    print("level: " + level)
    print("message: " + message)




file.close()