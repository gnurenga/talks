def gen_read_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line

for line in gen_read_file("syslog.txt"):
    print(line)
