import os, subprocess

print("Starting script")
static_ip = input("Enter static ip: ")
channel = 7
ssid = "temp"
password = "temp"
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

file_dnsmsq = open("/etc/dnsmsq.conf", "r")
file_safe = open("/etc/dnsmsq.conf.orig", "w")
file_safe = file_dnsmsq
file_safe.close()
file_dnsmsq.close()
open("/etc/dnsmsq.conf", "w").close()
dnsmsq = open("/etc/dnsmsq.conf", "w")
dnsmsq.write("interface=wlan0 \n"
             "dhcp-range=192.168.2.10, 192.168.2.40, 255.255.255.0,24h")
dnsmsq.close()
file_hostapd = open("/etc/hostapd/hostapd.conf", "w")
file_hostapd.write("interface=wlan0 \n "
                   "bridge=br0 \n "
                   "hw_mode=g \n "
                   "channel=" +channel+"\n"
                   "wmm_enabled=0 \n"
                   "macaddr_acl=0 \n"
                    "auth_algs=1 \n"
                    "ignore_broadcast_ssid=0 \n"
                    "wpa=2 \n"
                    "wpa_key_mgmt=WPA-PSK \n"
                    "wpa_pairwise=TKIP \n"
                    "rsn_pairwise=CCMP \n"
                    "ssid=" +ssid+" \n"
                    "wpa_passphrase="+password)
file_hostapd.close()
file_default_hostapd = open("/etc/default/hostapd" "rw")