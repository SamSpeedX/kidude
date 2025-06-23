import time, subprocess

LOG_FILE = "/var/log/nginx/access.log"
BAD_AGENTS = ["python-requests", "curl", "scrapy", "wget", "bot", "spider"]

def block_ip(ip):
    print(f"[BOTWATCH] Blocking: {ip}")
    subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

def is_bot(line):
    return any(agent in line.lower() for agent in BAD_AGENTS)

def start_bot_watcher():
    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.3)
                continue
            if is_bot(line):
                ip = line.split()[0]
                block_ip(ip)
