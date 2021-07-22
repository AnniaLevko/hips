
import os
import subprocess
import datetime



BLACK_LIST_SNIFFER_TOOLS = ["tcpdump", "ethereal", "wireshark"]
BLACK_LIST_LIBRARIES = ["libpcap"]

LOGS_NET_INT_PROMISCOUS_COMMAND = "cat /var/log/messages | grep -i promis"

NET_INT_TO_CHECK = ["lo", "virbr0", "virbr0-nic", "enp0s3"]

USERS_ALLOWED_TO_USE_SNIFFER_TOOLS = ["erwaen", "root"]

def log_promiscuo_mode(): 
    resultado_comando = os.popen(LOGS_NET_INT_PROMISCOUS_COMMAND).read().split("\n")
    resultado_comando.pop(-1)
    print(resultado_comando)
    print("\n\n")

log_promiscuo_mode()