***WARNING THIS PROGRAM CAN ACTUALLY HARM YOUR NETWORK/NETWORK DEVICES, CONSIDER WHAT YOU ARE DOING CARFULLY!***

# MiTM
Program-Representation of the MiTM attack.

# Requirements
A Linux device to run the program.

# Installation
First update and install git
```
sudo apt-get update
sudo apt install git
```
(If you dont have pip) ``` sudo apt install python3-pip ```
Install netifaces, scapy, colorama modules
```
pip3 install netifaces
sudo python3 -m pip install --pre scapy[complete]
pip3 install colorama
```
Then install the package
```
git clone https://github.com/eliran3/MiTM.git
```
Enter the directory "MiTM/src" and run the following
```
chmod +x MTM.py
```
All left to do is run the script!
```
sudo ./MTM.py
```

IMPORTANT: ``` ctrl+c ``` to exit the program.

***CURRENTLY WORKING ON cryptography.py***

Licensed under the [MIT License](LICENSE).
