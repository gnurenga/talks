def read_file(file_name):
    with open(file_name, 'r') as f:
        test = []
        for l in f:
            test.append(l)
    return test


#print(read_file('brew-installation-output.txt'))

k = read_file('syslog.txt')
print(k)

