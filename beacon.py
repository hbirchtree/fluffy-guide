from common import *
import time
import json

from broadcast import UdpBeacon
from network import network_enumerator
from hwmon_monitor import hwmon_enumerator
from system_stats import get_load_avg
from core_clocks import *


def get_system_info() -> Dict[str, Any]:
    base_data = {
        'hostname': socket.gethostname(),
        'load': [x for x in get_load_avg()],
        'networks': [],
        'sensors': [],
        'cores': []
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
    for core in core_enumerator():
        base_data['cores'].append({
            'freq_max': core.max,
            'freq_cur': core.current,
            'freq_min': core.min,
            'node': core.node,
            'governor': core.governor,
            'available_governors': core.available_governors,
            'sensor': core.max,
        })
    proc_info = processor_description()
    base_data['processor'] = {
        'manufacturer': proc_info.manufacturer,
        'model': proc_info.model,
        'architecture': proc_info.architecture,
    }
    system_info = system_description()
    base_data['system'] = {
        'variant': system_info.variant,
        'version': system_info.version,
        'machine': system_info.machine,
        'distro': system_info.distro,
        'distro_version': system_info.distro_version,
    }

    return base_data

if __name__ == '__main__':
    beacon = UdpBeacon()

    print(processor_description())
    print(system_description())
    print(get_system_info())

    while True:
        beacon.send(get_system_info())
        time.sleep(30.0)
