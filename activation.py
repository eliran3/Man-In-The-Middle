from virus import man_the_middle
from getpass import getpass
from colorama import Fore
from sys import stdout
from time import sleep
from ipscanner import ip_scan_in_network

def perform_activation():
    activation_key = getpass(Fore.RED + f'[*] Activation Key ')

    flag = False

    if activation_key != 'golo123':
        activation_key = getpass(Fore.RED + f'[*] Activation Key? ')

        if activation_key != 'golo123':
            exit()
        
        flag = True
    
    stdout.write("\033[F")
    
    if flag: stdout.write("\033[F")

    print(Fore.RED + '[-] Key Activated    ')

    for i in range(5):
        print(Fore.RED + f'[--] MiTMA in {5-i}     ')
        sleep(1)
        stdout.write("\033[F")
    
    stdout.write("\033[F")
    
    man_the_middle()
