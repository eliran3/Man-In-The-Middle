***WARNING THIS PROGRAM CAN ACTUALLY HARM YOUR NETWORK/NETWORK DEVICES, CONSIDER WHAT YOU ARE DOING CARFULLY!***

# Man-In-The-Middle
Program to perform MiTM attack on gateway.

# Requirements
A Linux device to run the program.

# Installation
First update and install git
```
sudo apt-get update
sudo apt install git
```
(If you dont have pip) ``` sudo apt install python3-pip ```
Install netifaces, scapy and colorama modules
```
pip3 install netifaces
sudo python3 -m pip install --pre scapy[complete]
pip3 install colorama
```
Then install the package
```
git clone https://github.com/eliran3/Man-In-The-Middle.git
```
Allow MTM.py executable permission
```
chmod +x MTM.py
```
All left to do is run the script!
```
sudo ./MTM.py
```

IMPORTANT: ``` ctrl+c ``` to exit the program.

Licensed under the [MIT License](LICENSE).
