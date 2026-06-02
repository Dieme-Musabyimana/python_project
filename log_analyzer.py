import sys

file_name = sys.argv[1]
file = open(file_name)

for line in file:
    print(line.strip())

file.close()