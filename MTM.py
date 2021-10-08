#! /usr/bin/python3

import src.utils as utils

from src.activation import perform_activation
from src.portscanner import perform_port_scan

def main():
    # Some information..
    utils.print_information()

    # Getting the default gateway of the network.
    gateway = utils.get_gateway()
    
    # Performing the first port scan.
    perform_port_scan(gateway, '1-60000')

    # Performing the MiTM attack activation.
    perform_activation()

if __name__ == '__main__':
    main()
