from netifaces import gateways, AF_INET
from colorama import Fore

def get_gateway():
    return gateways()['default'][AF_INET][0]

def print_information():
    print(Fore.CYAN + '\033[1m' + 'Copyright (c) @Eliran_Nissani, 2021' + '\033[1m')
    print(Fore.CYAN + '\033[1m' + 'GitHub Page: https://github.com/eliran3/Man-In-The-Middle.git' + '\033[1m')
    print(Fore.CYAN + '\033[1m' + '--------------------------------------------------------------' + '\033[1m')
