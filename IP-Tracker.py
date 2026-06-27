import os
import requests
import ipaddress
from datetime import datetime
import time
import sys
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# -------- LINKS --------
YOUTUBE = "https://www.youtube.com/@zerolytix"
INSTAGRAM = "https://instagram.com/zerolytix"
TIKTOK = "https://tiktok.com/@zerolytix"
GITHUB = "https://github.com/zerolytix"
TWITTER = "https://x.com/zerolytix"

opened = False
last_report = ""

# -------- CLEAR --------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# -------- OPEN YOUTUBE SILENT --------
def open_browser():
    try:
        subprocess.Popen(
            ["firefox", YOUTUBE],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass

# -------- PROMO --------
def promo():
    global opened
    print(Fore.CYAN + Style.BRIGHT + "ZEROLYTIX OSINT ENGINE STARTING...\n")

    print(Fore.YELLOW + "Connect:")
    print(Fore.GREEN + f"YouTube   : {YOUTUBE}")
    print(f"Instagram : {INSTAGRAM}")
    print(f"TikTok    : {TIKTOK}")
    print(f"GitHub    : {GITHUB}")
    print(f"Twitter X : {TWITTER}\n")

    if not opened:
        open_browser()
        opened = True

    time.sleep(1)

# -------- BANNER --------
def banner():
    print(Fore.RED + Style.BRIGHT + r"""
███████╗███████╗██████╗  ██████╗ ██╗     ██╗   ██╗████████╗██╗██╗  ██╗
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██║     ╚██╗ ██╔╝╚══██╔══╝██║╚██╗██╔╝
  ███╔╝ █████╗  ██████╔╝██║   ██║██║      ╚████╔╝    ██║   ██║ ╚███╔╝ 
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██║       ╚██╔╝     ██║   ██║ ██╔██╗ 
███████╗███████╗██║  ██║╚██████╔╝███████╗   ██║      ██║   ██║██╔╝ ██╗
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═╝
""" + Style.RESET_ALL)

    print(Fore.CYAN + Style.BRIGHT + "   ZEROLYTIX • IP OSINT CLI")
    print(Fore.WHITE + "-" * 60)
    print(Fore.MAGENTA + "YouTube | Instagram | TikTok | GitHub | Twitter X ➤ @zerolytix\n")

# -------- VALIDATION --------
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def check_ip_type(ip):
    ip_obj = ipaddress.ip_address(ip)
    if ip_obj.is_private:
        return "Private"
    elif ip_obj.is_reserved or ip_obj.is_loopback:
        return "Reserved"
    else:
        return "Public"

# -------- FETCH --------
def fetch_ip(ip):
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting,query"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return {"status": "fail", "message": "Network Error"}

# -------- LOADING --------
def loading(text):
    for i in range(3):
        sys.stdout.write(Fore.YELLOW + f"\r{text}{'.' * (i+1)}")
        sys.stdout.flush()
        time.sleep(0.4)
    print()

# -------- SAVE REPORT --------
def save_report():
    global last_report
    if not last_report:
        return

    choice = input(Fore.CYAN + "Save report as TXT? (y/n): ").lower()
    if choice == 'y':
        filename = f"IP_Report_{int(time.time())}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(last_report)
        print(Fore.GREEN + f"Saved ➤ {filename}")
        time.sleep(1)

# -------- SCAN --------
def scan(ip):
    global last_report

    clear()
    banner()

    print(Fore.GREEN + f"Target ➤ {ip}\n")

    loading("Fetching geo data")
    data = fetch_ip(ip)

    if data.get("status") != "success":
        print(Fore.RED + f"\nError: {data.get('message')}")
        return

    loading("Analyzing network")
    loading("Processing data")

    ip_type = check_ip_type(ip)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report = f"""
========== OSINT REPORT ==========

Time        : {timestamp}
IP          : {data['query']}
Type        : {ip_type}

[ Location ]
Country     : {data['country']} ({data['countryCode']})
Region      : {data['regionName']}
City        : {data['city']}
ZIP         : {data['zip']}
Coordinates : {data['lat']}, {data['lon']}
Map         : https://www.google.com/maps?q={data['lat']},{data['lon']}

[ Network ]
ISP         : {data['isp']}
Org         : {data['org']}
ASN         : {data['as']}

[ Flags ]
Mobile      : {'Yes' if data['mobile'] else 'No'}
Proxy/VPN   : {'Yes' if data['proxy'] else 'No'}
Hosting     : {'Yes' if data['hosting'] else 'No'}

=================================
"""

    last_report = report

    print(Fore.GREEN + report)
    print(Fore.MAGENTA + "Follow ➤ @zerolytix\n")

    save_report()

# -------- MAIN --------
promo()

while True:
    clear()
    banner()

    ip = input(Fore.WHITE + "Enter IP ➤ ").strip()

    if not is_valid_ip(ip):
        print(Fore.RED + "\nInvalid IP!")
        time.sleep(1.5)
        continue

    scan(ip)

    again = input(Fore.YELLOW + "Another scan? (y/n): ").lower()
    if again != 'y':
        break
