from common import *

def get_load_avg() -> Iterator[float]:
    load = read_string('/proc/loadavg')

    for v in load.split(' ')[:3]:
        yield float(v)
