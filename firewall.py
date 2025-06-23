import time, subprocess
LOG = "logs/blacklist.log"
blocked_ips = set()

def block(ip):
    if ip not in blocked_ips:
        print(f"[FIREWALL] Blocking IP: {ip}")
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        blocked_ips.add(ip)

def start_monitoring():
    with open(LOG, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if "BLOCK:" in line:
                ip = line.split("BLOCK:")[1].strip()
                block(ip)
