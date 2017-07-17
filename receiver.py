import broadcast
import os
import tempfile


__temp_file = ''
__temp_dir = ''


def create_comm_socket():
    global __temp_file
    global __temp_dir

    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'iot_beacon')

    __temp_file = temp_file
    __temp_dir = temp_dir

    os.mkfifo(temp_file)
    print('Creating FIFO socket at %s' % temp_file)
    return open(temp_file, mode='w')


def clear_socket_files():
    os.remove(__temp_file)
    os.rmdir(__temp_dir)


if __name__ == '__main__':
    try:
        with create_comm_socket() as output_socket:
            beacon_receiver = broadcast.UdpBeacon()
            while True:
                pkt = beacon_receiver.sock.recv(4096)
                print(pkt)

                output_socket.write(pkt.decode() + '\n')
                output_socket.flush()
    except:
        clear_socket_files()
