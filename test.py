import time


def type_time(v):
    return time.strftime(v)


day = int(type_time("%d"))
pr
print(type_time("%Y") + "-" + type_time("%m") + "-" + type_time("%d"))