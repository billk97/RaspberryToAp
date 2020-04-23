import os, subprocess

print("Starting script")
password = input("Enter password: ")
print("installing hostapt")
os.system("sudo apt install hostapt | y" )
os.system("sudo apt install dnsmasq | y" )
