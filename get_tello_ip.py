import netifaces
import socket
import netaddr
import threading
import time

def _receive_thread():
    """Listen to responses from the Tello.

    Runs as a thread, sets self.response to whatever the Tello last returned.

    """
    global response
    global tello_ip_list
    global m_socket
    while True:
        try:
            response, ip = m_socket.recvfrom(1024)
            ip = ''.join(str(ip[0]))
            if response.upper() == b'OK' and ip not in tello_ip_list:
                print('[Found_Tello]Found Tello.The Tello ip is:%s\n' % ip)
                tello_ip_list.append(ip)
                break


        except socket.error as exc:
            print("[Exception_Error]Caught exception socket.error : %s\n" % exc)

def find_available_tello(num):
    """
    Find available tello in server's subnets
    :param num: Number of Tello this method is expected to find
    :return: None
    """
    print('[Start_Searching]Searching for %s available Tello...\n' % num)

    global tello_ip_list
    subnets, address = get_subnets()
    possible_addr = []

    for subnet, netmask in subnets:
        for ip in netaddr.IPNetwork('%s/%s' % (subnet, netmask)):
            # skip local and broadcast
            if str(ip).split('.')[3] == '0' or str(ip).split('.')[3] == '255':
                continue
            possible_addr.append(str(ip))

    while len(tello_ip_list) < num:
        print('[Still_Searching]Trying to find Tello in subnets...\n')

        # delete already found Tello
        for tello_ip in tello_ip_list:
            if tello_ip in possible_addr:
                possible_addr.remove(tello_ip)
        # skip server itself
        for ip in possible_addr:
            if ip in address:
                continue

            try:
                m_socket.sendto(b'command', (ip, 8889))
            except Exception as e:
                continue
        time.sleep(5)

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
    return subnets, addr_list

def get_tello_ip():
    global m_socket
    global tello_ip_list

    m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    m_socket.bind(('', 8889))

    recv_thread = threading.Thread(target=_receive_thread)
    recv_thread.daemon = True
    recv_thread.start()

    tello_ip_list = []
    find_available_tello(1)
    m_socket.close()
    return tello_ip_list[0]

if __name__ == "__main__":
    get_tello_ip()
