import os, subprocess

print("Starting script")
static_ip = input("Enter static ip: ")
channel = 7
ssid = input("ssidName: ")
password = input("password")
print("installing hostapt")
os.system("sudo apt install hostapd")
print("installing dnsmasq")
os.system("sudo apt install dnsmasq")
os.system("sudo systemctl stop hostapd")
# opening file to write settings
file_dhcpcd = open("/etc/dhcpcd.conf", "a")
file_dhcpcd.write("\n interface wla0 \n"
           "static ip_address="+static_ip+"\n"
           "denyinterfaces eth0 \n"
           "denyinterfaces wlan0")
file_dhcpcd.close()

file_dnsmsq = open("/etc/dnsmasq.conf", "r")
file_safe = open("/etc/dnsmasq.conf.orig", "w")
file_safe = file_dnsmsq
file_safe.close()
file_dnsmsq.close()
open("/etc/dnsmasq.conf", "w").close()
dnsmsq = open("/etc/dnsmasq.conf", "w")
dnsmsq.write("interface=wlan0 \n"
             "dhcp-range=192.168.2.10, 192.168.2.40, 255.255.255.0,24h")
dnsmsq.close()
file_hostapd = open("/etc/hostapd/hostapd.conf", "w")
file_hostapd.write("interface=wlan0\n"
                   "bridge=br0\n"
                   "hw_mode=g\n"
                   "channel={}\n"
                   "wmm_enabled=0\n"
                   "macaddr_acl=0\n"
                    "auth_algs=1\n"
                    "ignore_broadcast_ssid=0\n"
                    "wpa=2\n"
                    "wpa_key_mgmt=WPA-PSK\n"
                    "wpa_pairwise=TKIP\n"
                    "rsn_pairwise=CCMP\n"
                    "ssid={}\n"
                    "wpa_passphrase={}".format(channel, ssid, password))
file_hostapd.close()
#file_default_hostapd = open("/etc/default/hostapd" "rw")
#sudo nano /etc/sysctl.conf
##net.ipv4.ip_forward=1 -> net.ipv4.ip_forward=1
# sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
# iptables-restore < /etc/iptables.ipv4.nat
# sudo apt-get install bridge-utils
# sudo brctl addbr br0
# sudo brctl addif br0 eth0
# sudo nano /etc/network/interfaces
#auto br0
#iface br0 inet manual
#bridge_ports eth0 wlan0
#sudo reboot