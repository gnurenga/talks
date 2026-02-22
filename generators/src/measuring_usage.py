from memory_profiler import memory_usage
from timeit import timeit



def read_file(file_name):
    with open(file_name, 'r') as f:
        content = []
        for line in f:
            content.append(line)
    return content

def gen_read_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line

def use_gen_function(_gen_function):
    for line in _gen_function:
        a = line


mem_usage = memory_usage((read_file,('syslog.txt',)))
print(f"Memory usage of normal function: {max(mem_usage) - min(mem_usage)} MB")


mem_usage = memory_usage((use_gen_function,(gen_read_file('syslog.txt'),)))
print(f"Memory usage of generator function: {max(mem_usage) - min(mem_usage)} MB")


# _time = timeit('read_file("syslog.txt")', setup='from __main__ import read_file', number=100)
# print(f"Normal function time: {_time}")
# _time = timeit('list(gen_read_file("syslog.txt"))', setup='from __main__ import gen_read_file', number=100)
# print(f"Generator function time: {_time}")
