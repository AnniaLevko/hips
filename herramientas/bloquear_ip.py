import os

# Bloqueamos una IP con iptables
def bloquear_ip(ip):
    os.system(f"sudo iptables -I INPUT -s {ip} -j DROP")
    os.system("sudo service iptables save")