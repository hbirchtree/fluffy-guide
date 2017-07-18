from typing import NamedTuple, List, Dict, Iterator, Any
from os.path import basename
from glob import glob
import socket
from platform import uname, linux_distribution, mac_ver, win32_ver


PLATFORM = uname().system


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

ProcessorDescription = NamedTuple('ProcessorDescription',
                                  [
                                      ('manufacturer', str),
                                      ('model', str),
                                      ('architecture', str)
                                  ])

SystemDescription = NamedTuple('SystemDescription',
                               [
                                   ('variant', str),
                                   ('version', str),
                                   ('machine', str),
                                   ('distro', str),
                                   ('distro_version', str),
                               ])

CoreDescription = NamedTuple('CoreDescription',
                             [
                                 ('max', float),
                                 ('current', float),
                                 ('min', float),
                                 ('node', str),
                                 ('governor', str),
                                 ('available_governors', List[str]),
                                 ('hwmon_sensor', str)
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