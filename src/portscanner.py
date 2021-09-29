#!/usr/bin/python3

import socket, multiprocessing

from timeit import timeit
from colorama import Fore

class Open_Port:
    def __init__(self, port: int, service):
        self.port = port
        self.service = service
    
    def __eq__(self, other):
        return self.port == other.port and self.service == other.service

    def show(self):
        p = len(str(self.port))
        if p == 1:
            print(Fore.LIGHTGREEN_EX + f'{self.port}           open         {self.service}')
        elif p == 2:
            print(Fore.LIGHTGREEN_EX + f'{self.port}          open         {self.service}')
        elif p == 3:
            print(Fore.LIGHTGREEN_EX + f'{self.port}         open         {self.service}')
        elif p == 4:
            print(Fore.LIGHTGREEN_EX + f'{self.port}        open         {self.service}')
        elif p == 5:
            print(Fore.LIGHTGREEN_EX + f'{self.port}       open         {self.service}')
        elif p == 6:
            print(Fore.LIGHTGREEN_EX + f'{self.port}      open         {self.service}')

def scan(target, port: int, queue):
    service = ''
    
    try:
        sock = socket.socket()
        sock.settimeout(0.75)
        sock.connect((target, port))
        
        if port <= 1024:
            try:
                service = socket.getservbyport(port)
            except:
                if socket.getfqdn(target) != target:
                    service = socket.getfqdn(target)
                else:
                    pass
        
        queue.put(Open_Port(port, service))
    except:
        pass

    sock.close()

def check_ip(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return socket.gethostbyname(ip)

def scan_loop(target, start_p: int, end_p: int, queue):
    while (start_p <= end_p):
        scan(target, start_p, queue)
        start_p += 1

def multiprocessing_scan(target, ports_amount: int, start_p: int, end_p: int, queue, jumps: int=150):
    if ports_amount < 700:
        jumps = 2
    
    start = start_p
    end = start_p + jumps
    processes = []
    processes_amount = int(ports_amount / jumps)
    remaining_ports = 0
    
    if ports_amount % jumps != 0:
        remaining_ports = ports_amount % jumps
    
    for _ in range(processes_amount):
        process = multiprocessing.Process(target=scan_loop, args=(target, start, end, queue))
        
        process.start()
        processes.append(process)
        
        start += jumps; end += jumps
    
    for process in processes:
        process.join()
    
    if remaining_ports != 0:
        start =  end_p - remaining_ports
        scan_loop(target, start, end_p, queue)
    else:
        start = start_p
        end = start_p + jumps
        scan_loop(target, start, end, queue)
    
    outputs = arrange_outputs(queue)
    
    for o in outputs:
        o.show()
    
    print(Fore.MAGENTA + f'[=] Scan Ended! [{target}]')

def regular_scan_loop(target, ports, queue):
    for p in ports:
        p = int(p)
        scan(target, p, queue)

    outputs = arrange_outputs(queue)
    
    for o in outputs:
        o.show()
    
    print(Fore.MAGENTA + f'[=] Scan Ended! [{target}]')

def arrange_outputs(queue):
    outputs = []
    
    while queue.empty() is False:
        outputs.append(queue.get())

    def IsExists(outputs, o):
        counter = 0
        for o1 in outputs:
            if o == o1:
                counter += 1
        
        return counter
    
    for o in outputs:
        if IsExists(outputs, o) > 1:
            counter = IsExists(outputs, o)
            for i in range(0, counter - 1):
                outputs.remove(o)

    for i in range(len(outputs)):
        for k in range(0, len(outputs) - i - 1):
            if outputs[k].port > outputs[k+1].port:
                temp = outputs[k]
                outputs[k] = outputs[k+1]
                outputs[k+1] = temp
    
    return outputs

def perform_port_scan(ip_address_es: str, ports_number: str):
    ip_address_es = ip_address_es.replace(' ', '')
    targets = ip_address_es.split(',')
    
    for target in targets:
        target = check_ip(target)
        ports_amount = 0; start_p = 0; end_p = 0
        queue = multiprocessing.Queue()

        print(Fore.MAGENTA + f'[=] Performing Port Scan... [{target}]')
        print(Fore.LIGHTBLACK_EX + 'PORT        STATE        SERVICE')
        print(Fore.LIGHTBLACK_EX + '--------------------------------')

        if ',' in ports_number and '-' not in ports_number:
            ports = ports_number.replace(' ', '')
            ports = ports_number.split(',')
            
            print(Fore.GREEN + f'[=] Scan for {target} took {timeit(lambda: regular_scan_loop(target, ports, queue), number=1):.2f} seconds')
            print(Fore.CYAN + '------------------------------------------------')
        elif '-' in ports_number and ',' not in ports_number:
            ports = ports_number.replace(' ', '')
            ports = ports_number.split('-')
            ports_amount = int(ports[1]) - int(ports[0])
            start_p = int(ports[0])
            end_p = int(ports[1])

            print(Fore.GREEN + f'[=] Scan for {target} took {timeit(lambda: multiprocessing_scan(target, ports_amount, start_p, end_p, queue), number=1):.2f} seconds')
            print(Fore.CYAN + '------------------------------------------------')
        else:
            raise ValueError
