# coding=utf-8
#!/usr/bin/env python3

from libs.check_modules import check_modules
from sys import exit
from os import _exit
from multiprocessing import Process, Queue
from colorama import Fore, Style
import random

check_modules()

from libs.logo import print_logo
from libs.utils import print_success, print_error, ask_question, print_status, parse_proxy_file
from libs.proxy_harvester import find_proxies
from libs.attack import report_profile_attack, report_video_attack

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def attack_process(target, proxies, report_func):
    if not proxies:
        for _ in range(10):
            report_func(target, None)
        return

    for proxy in proxies:
        report_func(target, proxy)

def start_attack(target, proxies, attack_type):
    if attack_type == 'profile':
        report_func = report_profile_attack
    elif attack_type == 'video':
        report_func = report_video_attack
    else:
        print_error("Invalid attack type.")
        return

    if not proxies:
        for k in range(5):
            p = Process(target=attack_process, args=(target, [], report_func))
            p.start()
            print_status(f"{k + 1}. Transaction Opened!")
        return

    proxy_chunks = list(chunks(proxies, 10))
    print_status(f"{attack_type.capitalize()} complaint attack is starting!\n")

    for i, proxy_list in enumerate(proxy_chunks):
        p = Process(target=attack_process, args=(target, proxy_list, report_func))
        p.start()
        print_status(f"{i + 1}. Transaction Opened!")

def main():
    print_success("Modules loaded!\n")
    proxies = []

    ret = ask_question("Would you like to use a proxy? [Y/N]")
    if ret.lower() == 'y':
        ret = ask_question("Would you like to collect your proxies from the internet? [Y/N]")
        if ret.lower() == 'y':
            print_status("Gathering proxy from the Internet! This may take a while.\n")
            proxies = find_proxies()
        elif ret.lower() == 'n':
            file_path = ask_question("Enter the path to your proxy list")
            proxies = parse_proxy_file(file_path)
        else:
            print_error("Answer not understood, exiting!")
            exit()

        print_success(f"{len(proxies)} proxies found!\n")
    elif ret.lower() != 'n':
        print_error("Answer not understood, exiting!")
        exit()

    print_status("1 - Report the profile.")
    print_status("2 - Report a video.")
    report_choice = ask_question("Please select the complaint method")

    if not report_choice.isdigit() or int(report_choice) not in [1, 2]:
        print_error("The answer is not understood.")
        exit(0)

    target = ask_question("Enter the username of the person you want to report" if int(report_choice) == 1 else "Enter the link of the video you want to report")
    attack_type = 'profile' if int(report_choice) == 1 else 'video'

    start_attack(target, proxies, attack_type)

if __name__ == "__main__":
    print_logo()
    try:
        main()
        print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\n\n" + Fore.RED + "[ * ] The program is closing!")
        print(Style.RESET_ALL)
        _exit(0)
