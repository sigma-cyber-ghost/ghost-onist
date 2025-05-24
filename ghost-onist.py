import re
import sys
import time
import requests
import random
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import shutil

init(autoreset=True)

# ========== CONFIG ========== #
TELEGRAM_CHANNEL = "https://t.me/Sigma_Ghost"
GITHUB_PROFILE = "https://github.com/sigma-cyber-ghost"
GITHUB_REPO = "https://github.com/sigma-cyber-ghost/ghost-onist"
YOUTUBE_CHANNEL = "https://www.youtube.com/@sigma_ghost_hacking"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64)",
]

COUNTRY_CODES = {
    "US": "+1", "UK": "+44", "IN": "+91", "PK": "+92", "CA": "+1", "AU": "+61",
    "FR": "+33", "DE": "+49", "IT": "+39", "ES": "+34", "RU": "+7", "BR": "+55",
    "CN": "+86", "JP": "+81", "KR": "+82", "AE": "+971", "SA": "+966", "EG": "+20",
    "NG": "+234", "MX": "+52", "ZA": "+27", "BD": "+880", "PH": "+63", "TH": "+66",
    "TR": "+90", "IR": "+98", "AR": "+54", "CO": "+57", "VN": "+84"
}

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    }

# ========== UI ========== #
def print_banner():
    width = shutil.get_terminal_size().columns
    banner = rf"""
{Fore.CYAN}
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗    ██████╗ ███╗   ██╗██╗███████╗████████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝   ██╔═══██╗████╗  ██║██║██╔════╝╚══██╔══╝
██║  ███╗███████║██║   ██║███████╗   ██║█████╗██║   ██║██╔██╗ ██║██║███████╗   ██║   
██║   ██║██╔══██║██║   ██║╚════██║   ██║╚════╝██║   ██║██║╚██╗██║██║╚════██║   ██║   
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║      ╚██████╔╝██║ ╚████║██║███████║   ██║   
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝       ╚═════╝ ╚═╝  ╚═══╝╚═╝╚══════╝   ╚═╝   
{Fore.RESET}
"""
    print("\n".join(line.center(width) for line in banner.split("\n")))
    print(f"{Fore.YELLOW}🔗 Telegram: {TELEGRAM_CHANNEL}")
    print(f"{Fore.YELLOW}👨💻 GitHub Profile: {GITHUB_PROFILE}")
    print(f"{Fore.YELLOW}📁 GitHub Repo: {GITHUB_REPO}")
    print(f"{Fore.RED}🔴 YouTube: {YOUTUBE_CHANNEL}\n")

def show_menu():
    print(f"{Fore.LIGHTCYAN_EX}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}                 SIGMA GHOST BLACKSIGHT               ")
    print(f"{Fore.LIGHTCYAN_EX}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.CYAN} [1] 🕵️  Username Presence + Metadata Scan")
    print(f"{Fore.CYAN} [2] 🧩 Dark Web Leak Lookup")
    print(f"{Fore.CYAN} [3] ☎️  Phone Number — Country Code Helper")
    print(f"{Fore.RED} [0] ❌ Exit")
    print(f"{Fore.LIGHTCYAN_EX}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

def show_country_codes():
    print(f"\n{Fore.LIGHTMAGENTA_EX}🌍 Supported Country Codes:")
    count = 0
    for country, code in COUNTRY_CODES.items():
        print(f"{Fore.YELLOW}{country}: {code}", end="   ")
        count += 1
        if count % 4 == 0:
            print()
    print()

# ========== SCANNERS ========== #
def get_profile_metadata(username, platform, base_url):
    try:
        r = requests.get(base_url, headers=get_headers(), timeout=10)
        if r.status_code == 200:
            bio = re.findall(r'(bio|description|about)[^>]*>([^<]+)<', r.text, re.IGNORECASE)
            followers = re.findall(r'(followers|subscribers)[^0-9]*([0-9,]+)', r.text, re.IGNORECASE)
            return {
                "platform": platform,
                "status": "LIVE",
                "url": base_url,
                "bio": bio[0][1] if bio else None,
                "followers": followers[0][1] if followers else None
            }
        else:
            return {"platform": platform, "status": "DEAD", "url": base_url}
    except Exception as e:
        return {"platform": platform, "status": "ERROR", "url": base_url, "error": str(e)}

def search_user_presence(username):
    platforms = {
        "Instagram": f"https://instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Telegram": f"https://t.me/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Facebook": f"https://facebook.com/{username}",
        "Keybase": f"https://keybase.io/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",
        "Behance": f"https://www.behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}"
    }

    results = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {
            executor.submit(get_profile_metadata, username, p, url): p
            for p, url in platforms.items()
        }
        for f in as_completed(futures):
            results.append(f.result())
    return results

def search_darkweb(query):
    try:
        url = f"https://ahmia.fi/search/?q={quote(query)}"
        r = requests.get(url, headers=get_headers(), timeout=10)
        results = re.findall(r'href="(http[s]?://[a-zA-Z0-9\.]+\.onion.*?)"', r.text)
        return list(set(results))
    except:
        return []

# ========== OUTPUT ========== #
def print_results(title, items):
    print(f"\n{Fore.BLUE}=== {title} ===")
    if not items:
        print(f"{Fore.RED}None found.")
        return
    for i in items:
        if isinstance(i, dict):
            print(f"{Fore.GREEN}- {i.get('platform')}: {i.get('status')}")
            print(f"{Fore.CYAN}  URL: {i.get('url')}")
            if i.get("bio"):
                print(f"{Fore.MAGENTA}  Bio: {i.get('bio')}")
            if i.get("followers"):
                print(f"{Fore.YELLOW}  Followers: {i.get('followers')}")
        else:
            print(f"{Fore.LIGHTMAGENTA_EX}- {i}")

# ========== MAIN LOOP ========== #
def main():
    print_banner()
    while True:
        show_menu()
        choice = input(f"\n{Fore.YELLOW}[?] Choose option: ")

        if choice == "0":
            print(f"{Fore.RED}Exiting...Now Check More Tools Babe.\n")
            break

        elif choice == "1":
            user = input(f"{Fore.GREEN}[+] Enter username: ")
            results = search_user_presence(user)
            print_results("Platform Scan with Metadata", results)

        elif choice == "2":
            query = input(f"{Fore.GREEN}[+] Enter email / username / phone for dark web scan: ")
            results = search_darkweb(query)
            print_results("Dark Web Results", results)

        elif choice == "3":
            show_country_codes()

        else:
            print(f"{Fore.RED}Invalid option. Try again.\n")

if __name__ == '__main__':
    main()
