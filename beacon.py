from common import *
import time
import json

from broadcast import UdpBeacon
from network import network_enumerator
from hwmon_monitor import hwmon_enumerator
from system_stats import get_load_avg


def get_system_info() -> Dict[str, Any]:
    base_data = {
        'hostname': socket.gethostname(),
        'load': [x for x in get_load_avg()],
        'networks': [],
        'sensors': []
    }
    for sensor in hwmon_enumerator():
        base_data['sensors'].append({
            'current': sensor.current,
            'max': sensor.max,
            'crit': sensor.critical,
            'label': sensor.label,
        })
    for intf in network_enumerator():
        base_data['networks'].append({
            'name': intf.name,
            'mac': intf.mac
        })
    return base_data

if __name__ == '__main__':
    beacon = UdpBeacon()

    while True:
        beacon.send(get_system_info())
        time.sleep(30.0)
