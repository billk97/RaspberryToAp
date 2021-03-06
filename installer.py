import os, subprocess

print("Starting script")
static_ip = input("Enter static ip: ")
channel = 7
ssid = input("ssidName: ")
password = input("password: ")
print("====== checking for updates ======")
os.system("sudo apt-get update -y")
print("====== upgrading ======")
os.system("sudo apt-get upgrade -y")
print("====== installing hostapt ======")
os.system("sudo apt install hostapd -y")
print("====== hostapd installed ======")
print("====== installing dnsmasq ======")
os.system("sudo apt install dnsmasq -y")
print("====== dnsmasq installed ======")
print("====== stoping hostapd ======")
os.system("sudo systemctl stop hostapd")
print("====== stoping dnsmasq ======")
os.system("sudo systemctl stop dnsmasq")
# opening file to write settings
print("====== opening /etc/dhcpcd.conf ======")
file_dhcpcd = open("/etc/dhcpcd.conf", "a")
file_dhcpcd.write("\n denyinterfaces eth0 \n denyinterfaces wlan0 \n \n interface br0 \n static ip_address={} \n".format(static_ip))
file_dhcpcd.close()
print("====== done /etc/dhcpcd.conf ======")
print("====== copping /etc/dnsmasq.conf -> /etc/dnsmasq.conf.orig ======")
file_dnsmsq = open("/etc/dnsmasq.conf", "r")
file_safe = open("/etc/dnsmasq.conf.orig", "w")
file_safe = file_dnsmsq
file_safe.close()
file_dnsmsq.close()
print("====== done coping ======")
open("/etc/dnsmasq.conf", "w").close()
print("====== editing /etc/dnsmaq.conf ======")
dnsmsq = open("/etc/dnsmasq.conf", "w")
dnsmsq.write("interface=wlan0 \n"
             "dhcp-range=192.168.2.10, 192.168.2.40, 255.255.255.0,24h\n")
dnsmsq.close()
print("====== done /etc/dnsmaq.conf ======")
print("====== editing /etc/hostapd/hostapd.conf ======")
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
print("====== done /etc/hostapd/hostapd.conf ======")
print("====== changing /etc/default/hostapd ======")
with open("/etc/default/hostapd", "r") as file_def_hostapd:
    file_content = file_def_hostapd.readlines()
file_def_hostapd.close()
file_content[12] = DAEMON_CONF="/etc/hostapd/hostapd.conf"
with open("/etc/default/hostapd", "w") as file_def_hostapd:
    file_def_hostapd.writelines(file_content)
file_def_hostapd.close()
print("====== done /etc/default/hostapd ======")
print("====== changing /etc/sysctl.conf ======")
with open("/etc/sysctl.conf", "r") as file_sysctl_conf:
    content_sysctl_conf = file_sysctl_conf.readlines()
file_sysctl_conf.close()
content_sysctl_conf[27] = "net.ipv4.ip_forward=1"
with open("/etc/sysctl.conf", "w") as file_sysctl_conf:
    file_sysctl_conf.writelines(content_sysctl_conf)
file_sysctl_conf.close()
print("====== done /etc/sysctl.conf ======")
print("====== setting iptables ======")
os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
os.system("sudo sh -c \"iptables-save > /etc/iptables.ipv4.nat\"")
print("====== setting /etc/rc.local ======")
file_rc_local = open("/etc/rc.local", "a")
file_rc_local.write("\n iptables-restore < /etc/iptables.ipv4.nat \n")
file_rc_local.close()
print("====== installing bridge-utils ======")
os.system("sudo apt-get install bridge-utils -y")
print("====== connecting interfacess ======")
os.system("sudo brctl addbr br0")
os.system("sudo brctl addif br0 eth0")
print("====== changing /etc/interfaces ======")
file_network_interfaces = open("/etc/network/interfaces", "a")
file_network_interfaces.write("auto br0 \n"
                              "iface br0 inet manual \n"
                              "bridge_ports eth0 wlan0 \n")
os.system("sudo rfkill unblock 0")
print("Done installation finished successfully")
print("if all gone well please reboot!!!")
