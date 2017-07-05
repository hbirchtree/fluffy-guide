from common import *
import fcntl
import struct

def network_enumerator() -> Iterator[NetInterface]:
    def get_address(intf: str) -> str:
        return '0.0.0.0'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pack = struct.pack('256s', intf[:15].encode())
        out = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, pack))
        return out

    def valid_prefix(intf: str) -> bool:
        for pfx in NETWORK_PREFIXES:
            if intf.startswith(pfx):
                return True
        return False

    network_interfaces = glob('/sys/class/net/*')

    for intf in network_interfaces:
        state = read_stringnl('%s/operstate' % (intf,))
        mac = read_stringnl('%s/address' % (intf,)).upper()
        intf_name = basename(intf)
        if state != 'up' or not valid_prefix(intf_name):
            continue
        yield NetInterface(intf_name, state,
                           get_address(intf_name),
                           mac)