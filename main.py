import requests
import pyfiglet
import json 
import colorama
from colorama import Fore, Style

def find_sub_domains(domain):
    found_sub_domains = []

    # Query crt.sh to find subdomains
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            sub_domains = set(item['name_value'] for item in data)

            for sub_domain in sub_domains:
                full_domain = sub_domain.strip()
                if not full_domain.startswith('*'):
                    try:
                        # Verify if the subdomain is active and get the status code
                        sub_response = requests.get(f"http://{full_domain}", timeout=5)
                        status_code = sub_response.status_code
                        found_sub_domains.append((full_domain, status_code))
                        print(f"Found: {full_domain} (Status: {status_code})")
                    except requests.ConnectionError:
                        pass
                    except requests.RequestException as e:
                        print(f"Error connecting to {full_domain}: {e}")
        else:
            print(f"Error fetching subdomains from crt.sh: HTTP {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching subdomains from crt.sh: {e}")

    return found_sub_domains



def print_banner():
    ascii_banner = pyfiglet.figlet_format("KURD", font="slant")
    print(ascii_banner)
    print(Fore.GREEN + "Create By Twanst Codes " + Style.RESET_ALL)
    print(Fore.GREEN + "Github::  https://github.com/TwanstCodess/subdomainfinder.git" + Style.RESET_ALL)

if __name__ == "__main__":
    colorama.init()  # Initialize colorama
    print_banner()
    domain = input(Fore.YELLOW + "Enter Domain (e.g., example.com): " + Style.RESET_ALL)
    found_sub_domains = find_sub_domains(domain)

    if found_sub_domains:
        print(Fore.GREEN + "\nDiscovered Subdomains:" + Style.RESET_ALL)
        for sub_domain, status in found_sub_domains:
            print(f"Subdomain: {Fore.YELLOW}{sub_domain}{Style.RESET_ALL}, Status: {Fore.GREEN}{status}{Style.RESET_ALL}")
    else:
        print(Fore.RED + "No subdomains found." + Style.RESET_ALL)