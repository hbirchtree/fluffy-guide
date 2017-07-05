from typing import NamedTuple, List, Dict, Iterator, Any
from os.path import basename
from glob import glob
import socket


NETWORK_PREFIXES = ['enp', 'eth',
                    'wlp', 'wlan']

HWMonSensor = NamedTuple('HWMonSensor',
                         [
                             ('label',str),
                             ('sensor', str),
                             ('current', float),
                             ('max', float),
                             ('critical', float),
                         ])

NetInterface = NamedTuple('NetInterface',
                          [
                              ('name', str),
                              ('state', str),
                              ('address', str),
                              ('mac', str)
                          ])


def read_string(fn: str) -> str:
    with open(fn, 'r') as f:
        return f.read()


def read_stringnl(fn: str) -> str:
    return read_string(fn).replace('\n', '')


def read_float(fn: str) -> float:
    return float(read_stringnl(fn))


def read_int(fn: str) -> int:
    return int(read_stringnl(fn))