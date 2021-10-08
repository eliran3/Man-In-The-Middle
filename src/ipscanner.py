import multiprocessing

from src.utils import get_gateway
from scapy.all import *

subdomain = get_gateway()[:len(get_gateway())-2]

def check_ip(index_ip: int, queue):
    ip = subdomain + '.' + str(index_ip)

    resp, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=4, retry=2)
    
    if resp:
        queue.put(ip)

def ip_scan_in_network():
    processes = []

    queue = multiprocessing.Queue()
    
    for i in range(0, 256):
        process = multiprocessing.Process(target=check_ip, args=(i, queue,))
        
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    ips = []

    while queue.empty() is False:
        ips.append(queue.get())
    
    return ips
