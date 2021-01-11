import tellopy
import netifaces
import socket
import netaddr
import threading
import time


def get_subnets():
    """
    Look through the server's internet connection and
    returns subnet addresses and server ip
    :return: list[str]: subnets
             list[str]: addr_list
    """
    subnets = []
    ifaces = netifaces.interfaces()
    addr_list = []
    for myiface in ifaces:
        addrs = netifaces.ifaddresses(myiface)

        if socket.AF_INET not in addrs:
            continue
        # Get ipv4 stuff
        ipinfo = addrs[socket.AF_INET][0]
        address = ipinfo['addr']
        netmask = ipinfo['netmask']

        # limit range of search. This will work for router subnets
        if netmask != '255.255.255.0':
            continue

        # Create ip object and get
        cidr = netaddr.IPNetwork('%s/%s' % (address, netmask))
        network = cidr.network
        subnets.append((network, netmask))
        addr_list.append(address)
    
    possible_addr = []

    for subnet, netmask in subnets:
        for ip in netaddr.IPNetwork('%s/%s' % (subnet, netmask)):
            # skip local and broadcast
            if str(ip).split('.')[3] == '0' or str(ip).split('.')[3] == '255':
                continue
            possible_addr.append(str(ip))

    return possible_addr, addr_list


class mTello(Tello):
    def __init__(self, ip):
        self.firstTime = True

        self.debug = False
        self.pkt_seq_num = 0x01e4
        self.port = port
        self.udpsize = 2000
        self.left_x = 0.0
        self.left_y = 0.0
        self.right_x = 0.0
        self.right_y = 0.0
        self.sock = None
        self.state = self.STATE_DISCONNECTED
        self.lock = threading.Lock()
        self.connected = threading.Event()
        self.video_enabled = False
        self.prev_video_data_time = None
        self.video_data_size = 0
        self.video_data_loss = 0
        self.log = log
        self.exposure = 0
        self.video_encoder_rate = 4
        self.video_stream = None
        self.wifi_strength = 0
        self.log_data = LogData(log)
        self.log_data_file = None
        self.log_data_header_recorded = False

        # video zoom state
        self.zoom = False

        # fast mode state
        self.fast_mode = False

        # File recieve state.
        self.file_recv = {}  # Map filenum -> protocol.DownloadedFile

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))
        self.sock.settimeout(2.0)

        tellopy.dispatcher.connect(self.__state_machine, dispatcher.signal.All)
        threading.Thread(target=self.__recv_thread).start()
        threading.Thread(target=self.__video_thread).start()

        possible_addr, addr_list = get_subnets()
        while self.firstTime:
            # skip server itself
            for ip in possible_addr:
                if ip in address:
                    continue

                try:
                    self.sock.sendto(b'command', (ip, 8889))
                except Exception as e:
                    continue
            time.sleep(5)

    def __recv_thread(self):
        sock = self.sock

        while self.state != self.STATE_QUIT:

            if self.state == self.STATE_CONNECTED:
                self.__send_stick_command()  # ignore errors

            try:
                data, server = sock.recvfrom(self.udpsize)
                log.debug("recv: %s" % byte_to_hexstring(data))
                if self.__process_packet(data) and self.firstTime:
                    self.tello_addr = (server, 8889)
                    self.firstTime = False
            except socket.timeout as ex:
                if self.state == self.STATE_CONNECTED:
                    log.error('recv: timeout')
                self.__publish(event=self.__EVENT_TIMEOUT)
            except Exception as ex:
                log.error('recv: %s' % str(ex))
                show_exception(ex)

        log.info('exit from the recv thread.')
