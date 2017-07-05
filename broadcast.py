import socket
import json

class UdpBeacon(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)

        self.broadcast_address = '255.255.255.255'
        self.broadcast_port = 55585

        self.socket().setsockopt(socket.SOL_SOCKET,
                                 socket.SO_REUSEADDR, 1)
        self.socket().setsockopt(socket.SOL_SOCKET,
                                 socket.SO_BROADCAST, 1)

        self.socket().bind((self.broadcast_address,
                            self.broadcast_port))

    def socket(self) -> socket.socket:
        return self.sock

    def send(self, jsonData: str) -> None:
        encoder = json.JSONEncoder()
        serialized = encoder.encode(jsonData).encode()
        self.sock.sendto(serialized, (self.broadcast_address,
                                      self.broadcast_port))