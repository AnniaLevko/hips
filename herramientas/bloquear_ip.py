import os

# Bloqueamos una IP con iptables
def bloquear_ip(ip):
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
    print("dssd")
    os.system("sudo service iptables save")