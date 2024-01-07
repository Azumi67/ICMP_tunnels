#
# ICMP tunnel Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# There may be some mistakes, please forgive me as I worked on it during my studies.
# This script is designed to simplify the configuration of ICMP Tunnel.
#
# Supported operating systems: Ubuntu 20, Debian 12
## I use the same imports and other stuff to speed up in creating the script
# you should only install colorama & netifaces
# Usage:
#   Run the script with root privileges.
#   Follow the on-screen prompts to install, configure, or uninstall the tunnel.
#
#
# Disclaimer:
# This script comes with no warranties or guarantees. Use it at your own risk.
import platform
import sys
import os
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import random
import string
import shutil
import netifaces as ni
import urllib.request
import zipfile
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')


if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')


def display_checkmark(message):
    print('\u2714 ' + message)


def display_error(message):
    print('\u2718 Error: ' + message)


def display_notification(message):
    print('\u2728 ' + message)


def display_loading():
    duration = 3
    end_time = time.time() + duration
    ball_width = 10
    ball_position = 0
    ball_direction = 1

    while time.time() < end_time:
        sys.stdout.write('\r\033[93mLoading, Please wait... [' + ' ' * ball_position + 'o' + ' ' * (ball_width - ball_position - 1) + ']')
        sys.stdout.flush()

        if ball_position == 0:
            ball_direction = 1
        elif ball_position == ball_width - 1:
            ball_direction = -1

        ball_position += ball_direction
        time.sleep(0.1)
    
    sys.stdout.write('\r' + ' ' * (len('Loading, Please wait...') + ball_width + 4) + '\r')
    sys.stdout.flush()
    display_notification("\033[96mIt might take a while...\033[0m")

    
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
     _____       _     _      
    / ____|     (_)   | |     
   | |  __ _   _ _  __| | ___ 
   | | |_ | | | | |/ _` |/ _ \\
   | |__| | |_| | | (_| |  __/
    \_____|\__,_|_|\__,_|\___|
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\033[1;96m
                  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣯⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣿⣿
                ⢺⣽⡿⣅⠹⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⡻⣿⣻⣿⣿⣿⣁⣴⢟⡻⠻⣯⣌⣿
          ⠔⢫⠆⣾⡿⢷⣮⣥⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠯⠝⠛⠉⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣏⣀⣙⡄⢿⣿⣿⣿⣿⣿⣿⣿⢟
       ⢀⠳⢒⣷⣿⣿⢱⡂⠜⣿⣿⣿⣿⣿⣿⣿⡿⢛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡱⠟⢀⡇⠸⣶⣿
       ⠈⢩⣣⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠏⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣭⡽⠟⠫⠅⣿⡿⢶⣿⠿⣻⣿⣿⣿⣿
         ⢠⣿⣿⣿⣿⣿⣉⠻⣿⣿⣿⣿⢏⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢤⠢⣀⣀⠤⢞⢟⣟⣒⣣⠼⡯⡟⢻⡥⡒⠘⣿
        ⢠⠋⣴⡿⡿⣿⡔⠻⣿⣿⣿⣿⣏⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀⣆⣐⣥⣴⣾⣿⣿⣿⣶⠊⣼⣀⣸⣧⣿⣿⣿⣽
       ⣠⣿⣾⡟⣤⣇⠘⣿⣷⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠄⢻⣿⣿⣿⣿⣿⣿⣽⣻⣿⣿⣿⣿⢿⡍⢻⣿⣿⡇
      ⣰⠏⣾⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⠃⠀⣀⠠⠤⠐⠒⠒⠓⠒⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠐⠒⠒⠒⠤⠤⣀⠀⠘⣿⣿⣿⣿⣿⣿⣷⡟⢰⡿⠻⣟⡚⠻⣷⣿
     ⣰⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠔⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢿⣿⣿⣿⣿⣿⢙⢲⡞⢀⡄⠈⡗⣲⣾⣿⣿⡟⠁
⠀   ⢠⠇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[1;96m⠀⠀⠀⠀⣀⣀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣾⣿⣷⣯⣼⣿⣿⣿⣿⣿⣿⣿⠀
   ⢀⡎⠀⠀⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏\033[1;91m⡀⠀⣎⣁⣤⣼⣖⣶⣦⣬⣑⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠖⣈⣭⣤⣴⣮⣭⣴⡦\033[1;96m⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⠿
⠀  ⡼⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇\033[1;91m⢧⣤⣾⡿⣿⣿⣿⣿⣯⣽⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣰⣾⢿⣿⣿⣿⣿⣙\033[1;96m⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡱⣎⡟⠀
  ⢰⠇⠀⠀⢸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[1;91m⡠⣾⣿⠟⠀⣿⣿⠛⢽⣿⡿⢿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠋⠧⣾⣿⡟⠻ ⣿⣿\033[1;96m⢿⣿⡟⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣿
⠀⠀⣿⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆\033[1;91m⠀⠙⠆⠀⠙⡘⠢⡘⠿⢃⡞⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣫⠳⡙⢿⠃⡚⣻\033[1;96m⢻⣿⣿⣿⣿⠴⠐⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⢸⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢺⡄\033[1;91m⠀⠀⢢⡀⠙⠢⢀⣀⠡⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠦⣄⣀⣁⠮⠃\033[1;96m⣸⣏⣺⣿⣿⠹⡎⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⣼⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠣⣷⠀\033[1;91m⠀⠉⠙⠛⠦⠲⠒⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠲⠦⠴⠶⠶⠊\033[1;96m⣿⠇⣼⣿⣿⡩⢛⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⣿⡇⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⣿⣿⡏⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢞⣿⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀⠀⠀
  \033[96m  ______   \033[1;94m _______  \033[1;92m __    \033[1;93m  _______     \033[1;91m    __      \033[1;96m  _____  ___  
 \033[96m  /    " \  \033[1;94m|   __ "\ \033[1;92m|" \  \033[1;93m  /"      \    \033[1;91m   /""\     \033[1;96m (\"   \|"  \ 
 \033[96m // ____  \ \033[1;94m(. |__) :)\033[1;92m||  |  \033[1;93m|:        |   \033[1;91m  /    \   \033[1;96m  |.\\   \    |
 \033[96m/  /    ) :)\033[1;94m|:  ____/ \033[1;92m|:  |  \033[1;93m|_____/   )   \033[1;91m /' /\  \   \033[1;96m |: \.   \\  |
\033[96m(: (____/ // \033[1;94m(|  /     \033[1;92m|.  | \033[1;93m //       /   \033[1;91m //  __'  \  \033[1;96m |.  \    \ |
 \033[96m\        / \033[1;94m/|__/ \   \033[1;92m/\  |\ \033[1;93m |:  __   \  \033[1;91m /   /  \\   \ \033[1;96m |    \    \|
 \033[96m \"_____ / \033[1;94m(_______) \033[1;92m(__\_|_)\033[1;93m |__|  \___) \033[1;91m(___/    \___) \033[1;96m\___|\____\)
"""
    print(logo)
def main_menu():
    try:
        while True:
            display_logo()
            border = "\033[93m+" + "="*70 + "+\033[0m"
            content = "\033[93m║            ▌║█║▌│║▌│║▌║▌█║ \033[92mMain Menu\033[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \033[92m            Join Opiran Telegram \033[34m@https://t.me/OPIranClub\033[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)
            

            print(border)
            print(footer)
            print(border)
            print("0. \033[91mServices Status\033[0m")
            print("00. \033[93mIncrease Limit[Optional]\033[0m")
            print("1. \033[96mAdd Native IPV6\033[0m")
            print("2. \033[92mPingTunnel ICMP\033[0m")
            print("3. \033[93mIcmptunnel\033[0m")
            print("4. \033[92mHans ICMP \033[0m")
            print("5. \033[96mFRP TCP + ICMPs \033[0m")
            print("6. \033[93mFRP UDP + ICMPs \033[0m")
            print("7. \033[94mStop | Restart Service \033[0m")
            print("8. \033[91mUninstall\033[0m")
            print("q. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            if choice == '0':
                status_menu()
            elif choice == '00':
                up_up()
            elif choice == '1':
                Native_menu()
            elif choice == '2':
                pingtunnel_menu()
            elif choice == '3':
                icmp_socat_menu()
            elif choice == '4':
                hans_menu()
            elif choice == '5':
                frp_icmp_menu()
            elif choice == '6':
                frp_icmp_udp()
            elif choice == '7':
                start_serv()
            elif choice == '8':
                uni_menu()
            elif choice == 'q':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()
        
def up_up():
    ulimit_setting = 'ulimit -n 65535'
    bashrc_path = os.path.expanduser('~/.bashrc')

    with open(bashrc_path, 'r') as f:
        existing_bashrc = f.read()

    if ulimit_setting not in existing_bashrc:
        with open(bashrc_path, 'a') as f:
            f.write('\n')
            f.write(ulimit_setting)
            f.write('\n')

    sysctl_conf_path = '/etc/sysctl.conf'
    sysctl_params = [
        'net.core.rmem_max=26214400',
        'net.core.rmem_default=26214400',
        'net.core.wmem_max=26214400',
        'net.core.wmem_default=26214400',
        'net.core.netdev_max_backlog=2048'
    ]

    with open(sysctl_conf_path, 'r') as f:
        existing_sysctl_conf = f.read()

    params_to_add = []
    for param in sysctl_params:
        if param not in existing_sysctl_conf:
            params_to_add.append(param)

    if params_to_add:
        with open(sysctl_conf_path, 'a') as f:
            f.write('\n')
            f.write('\n'.join(params_to_add))
            f.write('\n')
        try:
            subprocess.run(["sudo", "sysctl", "-p"], stderr=subprocess.DEVNULL, check=True)
            display_checkmark("\033[92mIt is Done!\033[0m")
        except subprocess.CalledProcessError:
            print("\033[91mAn error occurred while setting it up.\033[0m")
    else:
        display_checkmark("\033[92mIt was already Done.\033[0m")
        
def status_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mStatus Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mFRP \033[0m')
    print('2. \033[96mSocat \033[0m')
    print('3. \033[93mHaproxy \033[0m')
    print('4. \033[92mPingtunnel \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            frp_status()
            break
        elif server_type == '2':
            socat_status()
            break
        elif server_type == '3':
            haproxy_status()
            break
        elif server_type == '4':
            ping_status()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def haproxy_status():
    services = {
        'Service': 'haproxy.service',
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║             \033[92mHaproxy Status\033[93m                 ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            status_output = os.popen(f"systemctl is-active {service_name} 2>/dev/null").read().strip()

            if status_output == "active":
                status = "\033[92m✓ Active     \033[0m"
            else:
                status = "\033[91m✘ Inactive   \033[0m"

            if service == 'Service':
                display_name = '\033[93m     Server   \033[0m'
            else:
                display_name = service

            print(f"           \033[93m ║\033[0m    {display_name}:   |    {status:<10}   \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")
    
            
def socat_status():
    services = {
        'iran': 'portforwarding.service'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║             \033[92mSocat Status\033[93m                   ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            status_output = os.popen(f"systemctl is-active {service_name}").read().strip()

            if status_output == "active":
                status = "\033[92m✓ Active     \033[0m"
            else:
                status = "\033[91m✘ Inactive   \033[0m"

            if service == 'iran':
                display_name = '\033[93mIRAN Server   \033[0m'
            else:
                display_name = service

            print(f"           \033[93m ║\033[0m    {display_name}:   |    {status:<10}   \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")
    
            
def ping_status():
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))

    services = {
        'iran': 'iran-pingtunnel',
        'kharej': 'kharej-pingtunnel'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║             \033[92mPingTunnel Status\033[93m              ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            for i in range(num_configs):
                config_service_name = f"{service_name}-{i+1}.service"
                status_output = os.popen(f"systemctl is-active {config_service_name}").read().strip()

                if status_output == "active":
                    status = "\033[92m✓ Active     \033[0m"
                else:
                    status = "\033[91m✘ Inactive   \033[0m"

                if service == 'iran':
                    display_name = '\033[93mIRAN Server   \033[0m'
                elif service == 'kharej':
                    display_name = '\033[93mKharej Service\033[0m'
                else:
                    display_name = service

                print(f"           \033[93m ║\033[0m    {display_name} {i+1}:   |    {status:<10} \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error retrieving status for {service}: {e}")
            continue

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")
    
def frp_status():
    services = {
        'iran': 'azumifrps1.service',
        'kharej': 'azumifrpc1-kharej.service'
    }

    print("\033[93m            ╔════════════════════════════════════════════╗\033[0m")
    print("\033[93m            ║                 \033[92mFRP Status\033[93m                 ║\033[0m")
    print("\033[93m            ╠════════════════════════════════════════════╣\033[0m")

    for service, service_name in services.items():
        try:
            status_output = os.popen(f"systemctl is-active {service_name}").read().strip()

            if status_output == "active":
                status = "\033[92m✓ Active     \033[0m"
            else:
                status = "\033[91m✘ Inactive   \033[0m"

            if service == 'iran':
                display_name = '\033[93mIRAN Server   \033[0m'
            elif service == 'kharej':
                display_name = '\033[93mKharej Service\033[0m'
            else:
                display_name = service

            print(f"           \033[93m ║\033[0m    {display_name}:   |    {status:<10}   \033[93m ║\033[0m")

        except OSError as e:
            print(f"Error retrieving status for {service}: {e}")
            continue
          

    print("\033[93m            ╚════════════════════════════════════════════╝\033[0m")
            
def uni_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mUninstall Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mFRP Hans \033[0m')
    print('2. \033[92mFRP Icmp \033[0m')
    print('3. \033[93mHans  \033[0m')
    print('4. \033[93mIcmptunnel  \033[0m')
    print('5. \033[96mSocat \033[0m')
    print('6. \033[93mHaproxy \033[0m')
    print('7. \033[92mPingtunnel \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_hans_tcp()
            break
        elif server_type == '2':
            remove_icmp_tcp()
            break
        elif server_type == '3':
            remove_hans()
            break
        elif server_type == '4':
            remove_icmp()
            break
        elif server_type == '5':
            remove_socat()
            break
        elif server_type == '6':
            remove_hp()
            break
        elif server_type == '7':
            remove_ping()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
		

def reset_icmp():
    try:
        reset_ipv4 = False
        reset_ipv6 = False

        os.system("sysctl -w net.ipv4.icmp_echo_ignore_all=0")
        reset_ipv4 = True

        os.system("sudo sysctl -w net.ipv6.icmp.echo_ignore_all=0")
        reset_ipv6 = True

        if reset_ipv4 or reset_ipv6:
            display_checkmark("\033[92mICMP has been reset to default!\033[0m")
        else:
            display_notification("\033[93mICMP settings has been reset.\033[0m")
    except Exception as e:
        display_error("\033[91mAn error occurred: {}\033[0m".format(str(e)))
	    
def remove_ping():
    os.system("clear")
    display_notification("\033[93mRemoving Pingtunnels ...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    reset_icmp()
    try:
        if subprocess.call("test -f /root/pingtunnel", shell=True) == 0:
            subprocess.run("rm /root/pingtunnel", shell=True)

        pingtunnel_services = ["kharej-pingtunnel", "iran-pingtunnel"]  

        num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))

        for service_name in pingtunnel_services:
            for i in range(1, num_configs + 1):
                service_name_with_num = f"{service_name}-{i}"
                subprocess.run(f"systemctl disable {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl stop {service_name_with_num}.service > /dev/null 2>&1", shell=True)
                subprocess.run(f"rm /etc/systemd/system/{service_name_with_num}.service > /dev/null 2>&1", shell=True)
                time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_hp():
    os.system("clear")
    display_notification("\033[93mRemoving Haproxy ...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl stop haproxy > /dev/null 2>&1", shell=True)
        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        if subprocess.call("test -f /etc/haproxy/haproxy.cfg", shell=True) == 0:
            subprocess.run("rm /etc/haproxy/haproxy.cfg", shell=True)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_socat():
    os.system("clear")
    display_notification("\033[93mRemoving Socat  ...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl disable portforwarding.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop portforwarding.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/portforwarding.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_hans():
    os.system("clear")
    display_notification("\033[93mRemoving Hans ...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    reset_icmp()
    try:
        if subprocess.call("test -f /etc/hans.sh", shell=True) == 0:
            subprocess.run("rm /etc/hans.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/hans.sh\" | crontab -", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps1.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("ip link set dev icmp down > /dev/null", shell=True)

        print("Progress: ", end="")

        try:

            lsof_process = subprocess.Popen(["lsof", "/root/hans-1.1/hans"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lsof_output, lsof_error = lsof_process.communicate()

            if lsof_output:
                pid = lsof_output.decode().split('\n')[1].split()[1]
                subprocess.run(["kill", pid])

            subprocess.run(["rm", "-rf", "/root/hans-1.1"])
        except FileNotFoundError:
            print("Error: Directory '/root/hans-1.1' does not exist.")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def remove_hans_tcp():
    os.system("clear")
    display_notification("\033[93mRemoving Hans + FRP ...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    reset_icmp()
    try:
        if subprocess.call("test -f /etc/hans.sh", shell=True) == 0:
            subprocess.run("rm /etc/hans.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/hans.sh\" | crontab -", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps1.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("ip link set dev icmp down > /dev/null", shell=True)

        print("Progress: ", end="")

        try:

            lsof_process = subprocess.Popen(["lsof", "/root/hans-1.1/hans"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lsof_output, lsof_error = lsof_process.communicate()

            if lsof_output:
                pid = lsof_output.decode().split('\n')[1].split()[1]
                subprocess.run(["kill", pid])

            subprocess.run(["rm", "-rf", "/root/hans-1.1"])
        except FileNotFoundError:
            print("Error: Directory '/root/hans-1.1' does not exist.")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except Exception as e:
        print("An error occurred during uninstallation:", str(e))
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_icmp():
    os.system("clear")
    display_notification("\033[93mRemoving icmptunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    reset_icmp()
    try:
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp-iran.sh\" | crontab -", shell=True)
        subprocess.run("ip link set dev tun0 down > /dev/null", shell=True)
        subprocess.run("ip link set dev tun1 down > /dev/null", shell=True)
        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        try:
            lsof_process = subprocess.Popen(["lsof", "-t", "/root/icmptunnel/icmptunnel"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lsof_output, lsof_error = lsof_process.communicate()

            if lsof_output:
                pids = lsof_output.decode().split('\n')[:-1]
                for pid in pids:
                    subprocess.run(["kill", pid])

            subprocess.run(["rm", "-rf", "/root/icmptunnel"])
        except FileNotFoundError:
            print("Error: Directory '/root/icmptunnel' does not exist.")

        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp-iran.sh\" | crontab -", shell=True)
        display_checkmark("\033[92mUninstall completed!\033[0m")

        if os.path.isfile("/etc/icmp.sh"):
            os.remove("/etc/icmp.sh")
        if os.path.isfile("/etc/icmp-iran.sh"):
            os.remove("/etc/icmp-iran.sh")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def remove_icmp_tcp():
    os.system("clear")
    display_notification("\033[93mRemoving FRP + icmptunnel...\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    reset_icmp()
    try:
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp.sh\" | crontab -", shell=True)

        time.sleep(1)
        subprocess.run("systemctl disable azumifrpc1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrpc1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrpc1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/azumifrps1.service > /dev/null 2>&1", shell=True)
        subprocess.run("ip link set dev tun0 down > /dev/null", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        try:
            lsof_process = subprocess.Popen(["lsof", "-t", "/root/icmptunnel/icmptunnel"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lsof_output, lsof_error = lsof_process.communicate()

            if lsof_output:
                pids = lsof_output.decode().split('\n')[:-1]
                for pid in pids:
                    subprocess.run(["kill", pid])

            subprocess.run(["rm", "-rf", "/root/icmptunnel"])
        except FileNotFoundError:
            print("Error: Directory '/root/icmptunnel' does not exist.")

        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp.sh\" | crontab -", shell=True)

        display_checkmark("\033[92mUninstall completed!\033[0m")

        if os.path.isfile("/etc/icmp.sh"):
            os.remove("/etc/icmp.sh")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
		
def start_serv():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m SERVICES\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mRestart Pingtunnel SERVICE \033[0m')
    print('2. \033[93mStop Pingtunnel SERVICE \033[0m')
    print('3. \033[96mRestart FRP SERVICE \033[0m')
    print('4. \033[93mStop FRP SERVICE \033[0m')
    print('5. \033[92mRestart Socat SERVICE \033[0m')
    print('6. \033[96mStop Socat SERVICE \033[0m')
    print('7. \033[93mRestart Haproxy SERVICE \033[0m')
    print('8. \033[92mStop Haproxy SERVICE \033[0m')
    print('0. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            restart_serv()
            break
        elif server_type == '2':
            stop_serv()
            break
        elif server_type == '3':
            restart_frpserv()
            break
        elif server_type == '4':
            stop_frpserv()
            break
        elif server_type == '5':
            restart_socat()
            break
        elif server_type == '6':
            stop_socat()
            break
        elif server_type == '7':
            restart_hap()
            break
        elif server_type == '8':
            stop_hap()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')

def restart_hap():
    os.system("clear")
    display_notification("\033[93mRestarting \033[92mHaproxy\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart haproxy.service > /dev/null 2>&1", shell=True)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop_hap():
    os.system("clear")
    display_notification("\033[93mStopping \033[92mHaproxy\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop haproxy.service > /dev/null 2>&1", shell=True)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip()) 
        
def restart_socat():
    os.system("clear")
    display_notification("\033[93mRestarting \033[92mSocat\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart portforwarding.service > /dev/null 2>&1", shell=True)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop_socat():
    os.system("clear")
    display_notification("\033[93mStopping \033[92mSocat\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop portforwarding.service > /dev/null 2>&1", shell=True)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())        
        
def restart_serv():
    os.system("clear")
    display_notification("\033[93mRestarting \033[92mPingTunnel\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart kharej-pingtunnel.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart iran-pingtunnel.service > /dev/null 2>&1", shell=True)
        time.sleep(1)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop_serv():
    os.system("clear")
    display_notification("\033[93mStopping \033[92mPingTunnel\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop iran-pingtunnel.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop kharej-pingtunnel.service > /dev/null 2>&1", shell=True)
        time.sleep(1)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())    
        
def restart_frpserv():
    os.system("clear")
    display_notification("\033[93mRestarting \033[92mFRP\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl restart azumifrps1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl restart azumifrpc1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mRestart completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
        
def stop_frpserv():
    os.system("clear")
    display_notification("\033[93mStopping \033[92mFRP\033[93m..\033[0m")
    print("\033[93m╭─────────────────────────────────────────────╮\033[0m")

    try:
        subprocess.run("systemctl daemon-reload", shell=True)
        subprocess.run("systemctl stop azumifrps1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl stop azumifrpc1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)


        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mService Stopped!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())        
        
def frp_icmp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mFRP + ICMPs | \033[92mTCP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mHans ICMP  + FRP\033[0m')
    print('2. \033[93mIcmptunnel + FRP \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hans_tcp_menu()
            break
        elif server_type == '2':
            icmp_tcp_menu()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')

    
def frp_menu():
    def stop_loading():
        display_error("\033[91mInstallation process interrupted.\033[0m")
        exit(1)


    arch = subprocess.check_output('uname -m', shell=True).decode().strip()

    if arch in ['x86_64', 'amd64']:
        frp_download_url = "https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_amd64.tar.gz"
        frp_directory_name = "frp_0.52.3_linux_amd64"
    elif arch in ['aarch64', 'arm64']:
        frp_download_url = "https://github.com/fatedier/frp/releases/download/v0.52.3/frp_0.52.3_linux_arm64.tar.gz"
        frp_directory_name = "frp_0.52.3_linux_arm64"
    else:
        display_error(f"Unsupported CPU architecture: {arch}")
        return

    display_notification("\033[93mDownloading FRP...\033[0m")

    try:
        subprocess.run(['wget', '-O', '/root/frp.tar.gz', frp_download_url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        display_checkmark("\033[92mFRP downloaded successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        display_error(f"An error occurred while downloading FRP: {str(e)}")
        return

    try:
        subprocess.run(['tar', '-xf', '/root/frp.tar.gz', '-C', '/root'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['rm', '/root/frp.tar.gz'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        display_error(f"An error occurred while extracting the FRP archive: {str(e)}")
        return

    old_dir_path = f'/root/{frp_directory_name}'
    new_dir_path = '/root/frp'

    try:
        if os.path.exists(new_dir_path):
            shutil.rmtree(new_dir_path)
        os.rename(old_dir_path, new_dir_path)
        display_checkmark("\033[92mFRP downloaded and installed successfully!\033[0m")
    except Exception as e:
        display_error(f"An error occurred while moving frp: {str(e)}")
        return


    display_checkmark("\033[92mIP forward enabled!\033[0m")
    display_loading()


def install_menu():

    display_notification("\033[93mInstalling \033[92mFRP\033[93m...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    frp_menu()
	

def iran_tcp_menu():

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────────╮\033[0m")
    local_ports = input("\033[93mEnter \033[92mlocal\033[93m Port|\033[96mPorts\033[93m (\033[0mcomma-separated\033[93m): \033[0m")
    remote_ports = input("\033[93mEnter \033[92mremote\033[93m Port|\033[96mPorts\033[93m (\033[0mcomma-separated\033[93m): \033[0m")

    print("\033[93m╰─────────────────────────────────────────────────────────────╯\033[0m")


    if os.path.exists("/root/frp/frps.toml"):
        os.remove("/root/frp/frps.toml")
    

    with open("/root/frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default 443): \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumichwan\n")
        f.write("\n")
        f.write("[v2ray]\n")
        f.write("type = tcp\n")
        f.write("local_ip = 127.0.0.1\n")
        f.write("local_port = {}\n".format(local_ports))
        f.write("remote_port = {}\n".format(remote_ports))
        f.write("use_encryption = true\n")
        f.write("use_compression = true\n")
        f.write("\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    service_name = "azumifrps1"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        
    

    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("systemctl enable {}".format(service_name))
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl restart {}".format(service_name))

    display_checkmark("\033[92mFRP Service Started!\033[0m")


def kharej_tcp_menu():


    frpc_ini_path = "/root/frp/frpc.toml"

    if os.path.exists(frpc_ini_path):
        os.remove(frpc_ini_path)
    display_notification("\033[93mConfiguring \033[92mFRP\033[93m...\033[0m")
    print("\033[93m──────────────────────────────────────────────────────────────────────────\033[0m")
    num_ports = int(input("\033[93mHow many \033[92mconfigs\033[93m do you have?: \033[0m"))
    time.sleep(1)
    
    iran_ipv6 = "80.1.2.100"

    with open(frpc_ini_path, "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumichwan\n")

    for i in range(1, num_ports + 1):
        kharej_port = input("\033[93mEnter \033[92mLocal \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        iran_port = input("\033[93mEnter \033[92mRemote \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        print("\033[93m──────────────────────────────────────────────────────────────────────────\033[0m")

        with open(frpc_ini_path, "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(i))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(kharej_port))
            f.write("remote_port = {}\n".format(iran_port))
            f.write("local_ip = 127.0.0.1\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")


    display_checkmark("\033[92mKharej configuration generated. Yours Truly, Azumi.\033[0m")

    with open("/etc/systemd/system/azumifrpc1.service", "w") as f:
        f.write("[Unit]\n")
        f.write("Description=frpc service\n")
        f.write("After=network.target\n")
        f.write("\n")
        f.write("[Service]\n")
        f.write("ExecStart=/root/frp/./frpc -c /root/frp/frpc.toml\n")
        f.write("Restart=always\n")
        f.write("RestartSec=10\n")
        f.write("User=root\n")
        f.write("\n")
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")


    os.system("systemctl daemon-reload")
    os.system("systemctl enable azumifrpc1")
    os.system("sudo chmod u+x /etc/systemd/system/azumifrpc1.service")
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl restart azumifrpc1")

    display_checkmark("\033[92mFRP Service Started!\033[0m") 
    
def hans_tcp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mFRP + Hans | \033[92mTCP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hanss_kharej_menu()
            break
        elif server_type == '2':
            hanss_iran_menu()
            break
        elif server_type == '3':
            os.system('clear')
            frp_icmp_menu()
            break
        else:
            print('Invalid choice.')
            
def hanss_install_menu():
    display_notification("\033[93mInstalling \033[92mHans\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_loading()


    ipv4_forward_status = subprocess.run(["sysctl", "-n", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if int(ipv4_forward_status.stdout) != 1:
        subprocess.run(["sysctl", "net.ipv4.ip_forward=1"])

    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)

    subprocess.run(["wget", "https://sourceforge.net/projects/hanstunnel/files/source/hans-1.1.tar.gz"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["tar", "-xzf", "hans-1.1.tar.gz"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.chdir("/root/hans-1.1")

    subprocess.run(["apt", "install", "-y", "make"], check=True)
    subprocess.run(["apt", "install", "-y", "g++"], check=True)
    subprocess.run(["make"], check=True)

    display_checkmark("\033[92mHans installed successfully!\033[0m")

    os.remove("/root/hans-1.1.tar.gz")
    pass
    
##later
def generate_password(length=10):
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return password


def hanss_kharej_menu():
    if not os.path.exists("/root/hans-1.1"):
        hanss_install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[92mKharej\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    hans_directory = "/root/hans-1.1"

    os.chdir(hans_directory)
    os.system(f"./hans -s 80.1.2.0 -p azumi86chwan -d icmp")


    subprocess.call(["crontab", "-r", "-u", "root"])


    hans_kharej_command = f"{hans_directory}/hans -s 80.1.2.0 -p azumi86chwan -d icmp"
    subprocess.run(["sed", "-i", f"/{hans_kharej_command}/d", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)


    if os.path.exists("/etc/hans.sh"):
        os.remove("/etc/hans.sh")


    with open("/etc/hans.sh", "w") as f:
        f.write(f"{hans_kharej_command}\n")


    subprocess.run(["chmod", "700", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)


    cron_job_command = f"@reboot /bin/bash /etc/hans.sh\n"
    with open("/etc/cron.d/hans-kharej", "w") as f:
        f.write(cron_job_command)


    subprocess.call("crontab -u root /etc/cron.d/hans-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/frp"):
        install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    kharej_tcp_menu()
    iran_config_done = input("\033[96m Has IRAN config been done? (\033[92myes\033[93m/\033[91mno\033[96m): \033[0m")
    if iran_config_done.lower() in ["yes", "y"]:
        subprocess.run(["systemctl", "restart", "azumifrpc1"])

	
def hanss_iran_menu():
    if not os.path.exists("/root/hans-1.1"):
        hanss_install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[92mIRAN\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")

    os.chdir("/root/hans-1.1")
    os.system(f"./hans -c {server_ipv4} -p azumi86chwan -d icmp")


    os.system("ping -c 3 80.1.2.1")


    subprocess.call(["rm", "-f", "/etc/cron.d/hans"])


    hans_command = f"/root/hans-1.1/hans -c {server_ipv4} -p azumi86chwan -d icmp"
    subprocess.run(["sed", "-i", f"/{hans_command}/d", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)


    if os.path.exists("/etc/hans.sh"):
        os.remove("/etc/hans.sh")


    with open("/etc/hans.sh", "w") as f:
        f.write(f"{hans_command}\n")


    cron_job_command = f"@reboot root /bin/bash /etc/hans.sh\n"
    with open("/etc/cron.d/hans-iran", "w") as f:
        f.write(cron_job_command)


    subprocess.call("crontab -u root /etc/cron.d/hans-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/frp"):
        install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    iran_tcp_menu()
        
def icmp_tcp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIcmptunnel + FRP | \033[92mTCP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[96mIRAN \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            icmp_frp_kharej()
            break
        elif server_type == '2':
            icmp_frp_iran()
            break
        elif server_type == '3':
            os.system("clear")
            frp_icmp_menu()
            break
        else:
            print('Invalid choice.')
            
def install_icmp():
    display_notification("\033[93mInstalling \033[92mIcmptunnel\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_loading()


    ipv4_forward_status = subprocess.run(["sysctl", "-n", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if int(ipv4_forward_status.stdout) != 1:
        subprocess.run(["sysctl", "net.ipv4.ip_forward=1"])

    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)

    if os.path.exists("/root/icmptunnel"):
        shutil.rmtree("/root/icmptunnel")

    clone_command = 'git clone https://github.com/jamesbarlow/icmptunnel.git icmptunnel'
    clone_result = os.system(clone_command)
    if clone_result != 0:
        print("Error: Failed to clone Repo.")
        return

    if os.path.exists("/root/icmptunnel"):
        os.chdir("/root/icmptunnel")

        subprocess.run(['sudo', 'apt', 'install', '-y', 'net-tools'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'make'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libssl-dev'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'g++'], capture_output=True, text=True)

        subprocess.run(['make'], capture_output=True, text=True)

        os.chdir("..")
    else:
        display_error("\033[91micmptunnel folder not found.\033[0m")
    pass
        
def kharejj_tcp_menu():


    frpc_ini_path = "/root/frp/frpc.toml"

    if os.path.exists(frpc_ini_path):
        os.remove(frpc_ini_path)
    display_notification("\033[93mConfiguring \033[92mFRP\033[93m...\033[0m")
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────╮\033[0m")
    num_ports = int(input("\033[93mHow many \033[92mconfigs\033[93m do you have?: \033[0m"))
    time.sleep(1)
    
    iran_ipv6 = "70.0.0.2"

    with open(frpc_ini_path, "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumichwan\n")

    for i in range(1, num_ports + 1):
        kharej_port = input("\033[93mEnter \033[92mLocal \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        iran_port = input("\033[93mEnter \033[92mRemote \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        print("\033[93m────────────────────────────────────────────────────────────────────────────\033[0m")

        with open(frpc_ini_path, "a") as f:
            f.write("\n")
            f.write("[v2ray{}]\n".format(i))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(kharej_port))
            f.write("remote_port = {}\n".format(iran_port))
            f.write("local_ip = 127.0.0.1\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")


    display_checkmark("\033[92mKharej configuration generated. Yours Truly, Azumi.\033[0m")

    with open("/etc/systemd/system/azumifrpc1.service", "w") as f:
        f.write("[Unit]\n")
        f.write("Description=frpc service\n")
        f.write("After=network.target\n")
        f.write("\n")
        f.write("[Service]\n")
        f.write("ExecStart=/root/frp/./frpc -c /root/frp/frpc.toml\n")
        f.write("Restart=always\n")
        f.write("RestartSec=10\n") 
        f.write("User=root\n")
        f.write("\n")
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")


    os.system("systemctl daemon-reload")
    os.system("systemctl enable azumifrpc1")
    os.system("sudo chmod u+x /etc/systemd/system/azumifrpc1.service")
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl restart azumifrpc1")

    display_checkmark("\033[92mFRP Service Started!\033[0m") 
    
def icmp_frp_kharej():
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()

    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mconfiguring \033[92mKharej\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    if os.path.exists("/etc/icmp.sh"):
        os.remove("/etc/icmp.sh")

    with open("/etc/icmp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/root/icmptunnel/icmptunnel -s -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.1 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp.sh\n"
    with open("/etc/cron.d/icmp-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")

    if not os.path.exists("/root/frp"):
        install_menu()

    print("\033[93m──────────────────────────────────────────────────\033[0m")
    kharejj_tcp_menu()

    iran_config_done = input("\033[96m Has IRAN config been done? (\033[92myes\033[93m/\033[91mno\033[96m): \033[0m")
    if iran_config_done.lower() in ["yes", "y"]:
        subprocess.run(["systemctl", "restart", "azumifrpc1"])

def icmp_frp_iran():
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[92mIRAN\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.chdir("/root/icmptunnel")
    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")

    if os.path.exists("/etc/icmp-iran.sh"):
        os.remove("/etc/icmp-iran.sh")

    with open("/etc/icmp-iran.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"/root/icmptunnel/icmptunnel {server_ipv4} -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.2 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp-iran.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp-iran.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp-iran.sh\n"
    with open("/etc/cron.d/icmp-iran", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/frp"):
        install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    iran_tcp_menu()

def frp_icmp_udp():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mFRP + ICMPs | \033[92mUDP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mHans ICMP  + FRP\033[0m')
    print('2. \033[93mIcmptunnel + FRP \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hans_udp_menu()
            break
        elif server_type == '2':
            icmp_udp_menu()
            break
        elif server_type == '3':
            os.system('clear')
            main_menu()
            break
        else:
            print('Invalid choice.')

def iran_udp_menu():
    display_notification("\033[93mConfiguring \033[92mIRAN\033[93m...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────────╮\033[0m")
    local_ports = input("\033[93mEnter \033[92mlocal\033[93m Port|\033[96mPorts\033[93m (\033[0mcomma-separated\033[93m): \033[0m")
    remote_ports = input("\033[93mEnter \033[92mremote\033[93m Port|\033[96mPorts\033[93m (\033[0mcomma-separated\033[93m): \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────────╯\033[0m")

    if os.path.exists("/root/frp/frps.toml"):
        os.remove("/root/frp/frps.toml")

    with open("/root/frp/frps.toml", "w") as f:
        f.write("[common]\n")
        bind_port = input("\033[93mEnter \033[92mTunnel Port\033[93m (default 443): \033[0m")
        if not bind_port:
            bind_port = "443"
        f.write("bind_port = {}\n".format(bind_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumichwan\n")
        f.write("\n")
        f.write("[wireguard]\n")
        f.write("type = udp\n")
        f.write("local_ip = 127.0.0.1\n")
        f.write("local_port = {}\n".format(local_ports))
        f.write("remote_port = {}\n".format(remote_ports))
        f.write("use_encryption = true\n")
        f.write("use_compression = true\n")
        f.write("\n")

    display_checkmark("\033[92mIRAN configuration generated. Yours Truly, Azumi.\033[0m")

    service_name = "azumifrps1"
    frps_path = "/root/frp/frps.toml"

    service_content = f'''[Unit]
Description=frps service
After=network.target

[Service]
ExecStart=/root/frp/./frps -c {frps_path}
Restart=always
RestartSec=10
User=root

[Install]
WantedBy=multi-user.target
'''

    service_path = "/etc/systemd/system/{}.service".format(service_name)

    with open(service_path, "w") as f:
        f.write(service_content)
        
    

    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl daemon-reload")
    os.system("systemctl enable {}".format(service_name))
    os.system("sudo chmod u+x /etc/systemd/system/{}.service".format(service_name))
    os.system("systemctl restart {}".format(service_name))

    display_checkmark("\033[92mFRP Service Started!\033[0m")


def kharej_udp_menu():


    frpc_ini_path = "/root/frp/frpc.toml"

    if os.path.exists(frpc_ini_path):
        os.remove(frpc_ini_path)
    display_notification("\033[93mConfiguring \033[92mFRP\033[93m...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────────────────────\033[0m")
    num_ports = int(input("\033[93mHow many \033[92mconfigs\033[93m do you have?: \033[0m"))
    time.sleep(1)
    
    iran_ipv6 = "80.1.2.100"

    with open(frpc_ini_path, "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumichwan\n")

    for i in range(1, num_ports + 1):
        kharej_port = input("\033[93mEnter \033[92mLocal \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        iran_port = input("\033[93mEnter \033[92mRemote \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        print("\033[93m────────────────────────────────────────────────────────────────────────\033[0m")

        with open(frpc_ini_path, "a") as f:
            f.write("\n")
            f.write("[wireguard{}]\n".format(i))
            f.write("type = udp\n")
            f.write("local_port = {}\n".format(kharej_port))
            f.write("remote_port = {}\n".format(iran_port))
            f.write("local_ip = 127.0.0.1\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")


    display_checkmark("\033[92mKharej configuration generated. Yours Truly, Azumi.\033[0m")

    with open("/etc/systemd/system/azumifrpc1.service", "w") as f:
        f.write("[Unit]\n")
        f.write("Description=frpc service\n")
        f.write("After=network.target\n")
        f.write("\n")
        f.write("[Service]\n")
        f.write("ExecStart=/root/frp/./frpc -c /root/frp/frpc.toml\n")
        f.write("Restart=always\n")
        f.write("RestartSec=10\n")
        f.write("User=root\n")
        f.write("\n")
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")


    os.system("systemctl daemon-reload")
    os.system("systemctl enable azumifrpc1")
    os.system("sudo chmod u+x /etc/systemd/system/azumifrpc1.service")
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl restart azumifrpc1")

    display_checkmark("\033[92mFRP Service Started!\033[0m") 
	
def hans_udp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mFRP + Hans | \033[92mUDP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hanss_kharej_udp()
            break
        elif server_type == '2':
            hanss_iran_udp()
            break
        elif server_type == '3':
            os.system('clear')
            frp_icmp_udp()
            break
        else:
            print('Invalid choice.')
			

def hanss_kharej_udp():
    if not os.path.exists("/root/hans-1.1"):
        hanss_install_menu()

    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[92mKharej\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    hans_directory = "/root/hans-1.1"

    os.chdir(hans_directory)
    os.system(f"./hans -s 80.1.2.0 -p azumi86chwan -d icmp")

    subprocess.call(["crontab", "-r", "-u", "root"])

    hans_kharej_command = f"{hans_directory}/hans -s 80.1.2.0 -p azumi86chwan -d icmp"
    subprocess.run(["sed", "-i", f"/{hans_kharej_command}/d", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)

    if os.path.exists("/etc/hans.sh"):
        os.remove("/etc/hans.sh")

    with open("/etc/hans.sh", "w") as f:
        f.write(f"{hans_kharej_command}\n")

    subprocess.run(["chmod", "700", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    cron_job_command = f"@reboot /bin/bash /etc/hans.sh\n"
    with open("/etc/cron.d/hans-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/hans-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")

    if not os.path.exists("/root/frp"):
        install_menu()

    print("\033[93m──────────────────────────────────────────────────\033[0m")
    kharej_udp_menu()

    iran_config_done = input("\033[96m Has IRAN config been done? (\033[92myes\033[93m/\033[91mno\033[96m): \033[0m")
    if iran_config_done.lower() in ["yes", "y"]:
        subprocess.run(["systemctl", "restart", "azumifrpc1"])

	
def hanss_iran_udp():
    if not os.path.exists("/root/hans-1.1"):
        hanss_install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring \033[92mIRAN\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address:\033[0m ")

    os.chdir("/root/hans-1.1")
    os.system(f"./hans -c {server_ipv4} -p azumi86chwan -d icmp")


    os.system("ping -c 3 80.1.2.1")


    subprocess.call(["rm", "-f", "/etc/cron.d/hans"])


    hans_command = f"/root/hans-1.1/hans -c {server_ipv4} -p azumi86chwan -d icmp"
    subprocess.run(["sed", "-i", f"/{hans_command}/d", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)


    if os.path.exists("/etc/hans.sh"):
        os.remove("/etc/hans.sh")


    with open("/etc/hans.sh", "w") as f:
        f.write(f"{hans_command}\n")


    cron_job_command = f"@reboot root /bin/bash /etc/hans.sh\n"
    with open("/etc/cron.d/hans-iran", "w") as f:
        f.write(cron_job_command)


    subprocess.call("crontab -u root /etc/cron.d/hans-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/frp"):
        install_menu()

    print("\033[93m──────────────────────────────────────────────────\033[0m")
    iran_udp_menu()
        
def icmp_udp_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIcmptunnel + FRP | \033[92mUDP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[93mKHAREJ \033[0m')
    print('2. \033[96mIRAN \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            icmp_fudp_kha()
            break
        elif server_type == '2':
            icmp_fudp_ir()
            break
        elif server_type == '3':
            os.system("clear")
            frp_icmp_udp()
            break
        else:
            print('Invalid choice.')
            
        
def kharejj_udp_menu():


    frpc_ini_path = "/root/frp/frpc.toml"

    if os.path.exists(frpc_ini_path):
        os.remove(frpc_ini_path)
    display_notification("\033[93mConfiguring \033[92mFRP\033[93m...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────────────────╮\033[0m")
    num_ports = int(input("\033[93mHow many \033[92mconfigs\033[93m do you have?: \033[0m"))
    time.sleep(1)
    
    iran_ipv6 = "70.0.0.2"

    with open(frpc_ini_path, "w") as f:
        f.write("[common]\n")
        f.write("server_addr = {}\n".format(iran_ipv6))
        server_port = input("\033[93mEnter \033[92mTunnel port\033[93m (default 443): \033[0m")
        if not server_port:
            server_port = "443"
        f.write("server_port = {}\n".format(server_port))
        f.write("authentication_mode = token\n")
        f.write("token = azumichwan\n")

    for i in range(1, num_ports + 1):
        kharej_port = input("\033[93mEnter \033[92mLocal \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        iran_port = input("\033[93mEnter \033[92mRemote \033[93mport for \033[92mConfig {}\033[93m: \033[0m".format(i))
        print("\033[93m──────────────────────────────────────────────────────────────────────\033[0m")

        with open(frpc_ini_path, "a") as f:
            f.write("\n")
            f.write("[wireguard{}]\n".format(i))
            f.write("type = tcp\n")
            f.write("local_port = {}\n".format(kharej_port))
            f.write("remote_port = {}\n".format(iran_port))
            f.write("local_ip = 127.0.0.1\n")
            f.write("use_encryption = true\n")
            f.write("use_compression = true\n")


    display_checkmark("\033[92mKharej configuration generated. Yours Truly, Azumi.\033[0m")

    with open("/etc/systemd/system/azumifrpc1.service", "w") as f:
        f.write("[Unit]\n")
        f.write("Description=frpc service\n")
        f.write("After=network.target\n")
        f.write("\n")
        f.write("[Service]\n")
        f.write("ExecStart=/root/frp/./frpc -c /root/frp/frpc.toml\n")
        f.write("Restart=always\n")
        f.write("RestartSec=10\n")   
        f.write("User=root\n")
        f.write("\n")
        f.write("[Install]\n")
        f.write("WantedBy=multi-user.target\n")


    os.system("systemctl daemon-reload")
    os.system("systemctl enable azumifrpc1")
    os.system("sudo chmod u+x /etc/systemd/system/azumifrpc1.service")
    display_notification("\033[93mStarting FRP service...\033[0m")
    os.system("systemctl restart azumifrpc1")

    display_checkmark("\033[92mFRP Service Started!\033[0m") 
    
def icmp_fudp_kha():
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mconfiguring ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    if os.path.exists("/etc/icmp.sh"):
        os.remove("/etc/icmp.sh")

    with open("/etc/icmp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/root/icmptunnel/icmptunnel -s -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.1 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp.sh\n"
    with open("/etc/cron.d/icmp-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/frp"):
        install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    kharejj_udp_menu()
    iran_config_done = input("\033[96m Has IRAN config been done? (\033[92myes\033[93m/\033[91mno\033[96m): \033[0m")
    if iran_config_done.lower() in ["yes", "y"]:
        subprocess.run(["systemctl", "restart", "azumifrpc1"])

def icmp_fudp_ir():
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.chdir("/root/icmptunnel")
    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address:\033[0m ")

    if os.path.exists("/etc/icmp-iran.sh"):
        os.remove("/etc/icmp-iran.sh")

    with open("/etc/icmp-iran.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"/root/icmptunnel/icmptunnel {server_ipv4} -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.2 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp-iran.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp-iran.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp-iran.sh\n"
    with open("/etc/cron.d/icmp-iran", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/frp"):
        install_menu()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    iran_udp_menu()
    
def Native_menu():
    subprocess.run("clear", shell=True)
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mNative IP Menu\033[0m")
    print("\033[92m \"-\"\033[93m═════════════════════\033[0m")
    display_logo2()
    print("\033[93m.-------------------------------------------------------------------------------------------------------.\033[0m")
    print("\033[93m| \033[92mIf it didn't work, please uninstall it and add extra IP manually  \033[0m")
    print("\033[93m|\033[0m  If you don't have native IPv6, please use a private IP instead.                                             \033[0m")
    print("\033[93m'-------------------------------------------------------------------------------------------------------'\033[0m")
    display_notification("\033[93mAdding extra Native IPv6 [Kharej]...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────╮\033[0m")

    try:
        interface = subprocess.run("ip route | awk '/default/ {print $5; exit}'", shell=True, capture_output=True, text=True).stdout.strip()
        ipv6_addresses = subprocess.run(f"ip -6 addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}' | cut -d'/' -f1", shell=True, capture_output=True, text=True).stdout.strip().split('\n')

        print("\033[92mCurrent IPv6 addresses on", interface + ":\033[0m")
        for address in ipv6_addresses:
            print(address)

        confirm = input("\033[93mAre these your current IPv6 addresses? (y/n): \033[0m")
        if confirm.lower() != "y":
            display_error("\033[91mAborted. Please manually configure the correct IPv6 addresses.\033[0m")
            return

        sorted_addresses = sorted(ipv6_addresses, reverse=True)
        additional_address = ""
        for i in range(len(sorted_addresses)):
            current_last_part = sorted_addresses[i].split(':')[-1]
            modified_last_part_hex = format(int(current_last_part, 16) + 1, '04x')
            modified_address = ":".join(sorted_addresses[i].split(':')[:-1]) + ":" + modified_last_part_hex

            if modified_address not in sorted_addresses:
                additional_address = modified_address
                break

        if not additional_address:
            display_error("\033[91mNo additional address to add.\033[0m")
            return

        subprocess.run(["ip", "addr", "add", f"{additional_address}/64", "dev", interface])

        script_file = "/etc/ipv6.sh"
        with open(script_file, "a") as file:
            file.write(f"ip addr add {additional_address}/64 dev {interface}\n")

        subprocess.run(["chmod", "+x", script_file])

        subprocess.run("crontab -l | grep -v '/etc/ipv6.sh' | crontab -", shell=True)

        display_notification("\033[93mAdding cronjob for the server..\033[0m")
        subprocess.run("(crontab -l 2>/dev/null; echo \"@reboot /bin/bash /etc/ipv6.sh\") | crontab -", shell=True)

        display_checkmark("\033[92mIPv6 addresses added successfully!\033[0m")
    except ValueError as e:
        display_error("\033[91mAn error occurred while adding IPv6 addresses:", str(e), "\033[0m")
        
def get_ipv4():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface.startswith('eth') or interface.startswith('en'):
            try:
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    ipv4 = addresses[ni.AF_INET][0]['addr']
                    return ipv4
            except KeyError:
                pass
    return None
    
def save_haproxy(config):
    config_path = "/etc/haproxy/haproxy.cfg"
    
    if os.path.exists(config_path):
        os.remove(config_path)
  
    with open(config_path, "w") as file:
        file.write(str(config))

def restart_haproxy():
    os.system("systemctl restart haproxy")
    display_checkmark("\033[92mHAProxy service restarted!\033[0m")
    
def install_haproxy():
    display_loading()
    os.system("apt-get install -y haproxy > /dev/null")
    display_checkmark("\033[92mHAProxy installation completed.!\033[0m")
    
def haproxy_tunnel2(ipv4_addresses, ipv4_ports, iran_port):
    config = f"""\
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # Default SSL material locations
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private

    # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE>
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log global
    mode tcp
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

frontend vless_frontend
    bind *:8443 transparent
    mode tcp
    default_backend azumi_backend

backend azumi_backend
    mode tcp
    balance roundrobin

"""
    
    for i in range(len(ipv4_addresses)):
        ipv4_address = ipv4_addresses[i]
        ipv4_port = ipv4_ports[i]
        config += f"    server azumi{i+1} {ipv4_address}:{ipv4_port} \n"
    return config    
        
def haproxy_tunnel(ipv6_addresses, ipv6_ports, iran_port):
    config = f"""\
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

    # Default SSL material locations
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private

    # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE>
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log global
    mode tcp
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http

frontend azumi_frontend
    bind :::8443 transparent
    mode tcp
    default_backend azumi_backend

backend azumi_backend
    mode tcp
    option http-keep-alive
"""
    
    for i in range(len(ipv6_addresses)):
        ipv6_address = ipv6_addresses[i]
        ipv6_port = ipv6_ports[i]
        config += f"    server azumi{i+1} {ipv6_address}:{ipv6_port}\n"
    
    return config

def haproxy_pingtunnel_v6():
    display_notification("\033[93mConfiguring Haproxy...\033[0m")
    install_haproxy()
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have:\033[0m "))
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ipv6_addresses = []
    ipv6_ports = []
    kharej_address = input("\033[93m" + "Enter \033[92mKharej\033[93m IPV6 address: " + "\033[0m")

    for i in range(num_configs):
        port = input("\033[93m" + f"Enter \033[96mKharej Port \033[93m{i+1}\033[93m: " + "\033[0m")

        ipv6_addresses.append(kharej_address)
        ipv6_ports.append(port)

    config = haproxy_tunnel(ipv6_addresses, ipv6_ports, port)

    save_haproxy(config)
    sleep(1)
    restart_haproxy()
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    display_checkmark("\033[92mHAProxy configuration file generated!\033[0m")

    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Config port: {current_ipv4} : 8443  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    else:
        display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
        
def haproxy_pingtunnel_v4():
    display_notification("\033[93mConfiguring Haproxy...\033[0m")
    install_haproxy()
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    num_configs = int(input("\033[93mHow many \033[92mConfigs\033[93m do you have:\033[0m "))
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ipv4_addresses = []
    ipv4_ports = []
    kharej_address = input("\033[93m" + "Enter \033[92mKharej\033[93m IPv4|IPV6 address: " + "\033[0m")

    for i in range(num_configs):
        port = input("\033[93m" + f"Enter \033[96mKharej Port \033[93m{i+1}\033[93m: " + "\033[0m")

        ipv4_addresses.append(kharej_address)
        ipv4_ports.append(port)

    config = haproxy_tunnel2(ipv4_addresses, ipv4_ports, port)

    save_haproxy(config)
    sleep(1)
    restart_haproxy()
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    display_checkmark("\033[92mHAProxy configuration file generated!\033[0m")

    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Config port: {current_ipv4} : 8443  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    else:
        display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
   
        
def pingtunnel_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPingTunnel Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[96mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ping()
            break
        elif server_type == '2':
            iran_ping()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')  
            
def ignore():
    icmpv4_status = subprocess.run(["sysctl", "net.ipv4.icmp_echo_ignore_all"], capture_output=True, text=True)
    if "net.ipv4.icmp_echo_ignore_all = 1" not in icmpv4_status.stdout:
        subprocess.run(["sudo", "sh", "-c", "echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all"])

    icmpv6_status = subprocess.run(["sysctl", "net.ipv6.icmp.echo_ignore_all"], capture_output=True, text=True)
    if "net.ipv6.icmp.echo_ignore_all = 0" not in icmpv6_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.icmp.echo_ignore_all=1"])

    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])

    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])


def install_pingtunnel():
    display_notification("\033[93mInstalling PingTunnel ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[94m")
    
    
    subprocess.run(["sudo", "apt", "install", "wget", "zip", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    arch = platform.machine()
    if 'aarch64' in arch:
        download_link = "https://github.com/Azumi67/pingtunnel/releases/download/2.8/pingtunnel_linux_arm64.zip"
    else:
        download_link = "https://github.com/Azumi67/pingtunnel/releases/download/2.8/pingtunnel_linux_amd64.zip"
        
    subprocess.run(["wget", "-O", "pingtunnel.zip", download_link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    i = 0
    while True:
        time.sleep(0.5)
        if os.path.exists("pingtunnel.zip"):
            break
        i += 1
        loading_bar = "[" + "=" * i + " " * (10 - i) + "]"
        print(f"\r{loading_bar}", end="", flush=True)
    
    display_checkmark("\033[92mPingtunnel downloaded!\033[0m")
    
    subprocess.run(["sudo", "unzip", "pingtunnel.zip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    display_checkmark("\033[92mPingtunnel installed!\033[0m")
    
    os.remove("pingtunnel.zip")
    pass

def kharej_ping():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mKharej\033[93m PingTunnel Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIPV4 \033[0m')
    print('2. \033[93mIPV6 \033[0m')
    print('3. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            ipv4_kharej()
            break
        elif server_type == '2':
            ipv6_kharej()
            break
        elif server_type == '3':
            os.system("clear")
            pingtunnel_menu()
            break
        else:
            print('Invalid choice.') 
            
def stop_n_remove_service(service_name):
    service_file = f'/etc/systemd/system/{service_name}.service'
    if os.path.exists(service_file):
        subprocess.run(['sudo', 'systemctl', 'stop', service_name], capture_output=True)
        subprocess.run(['sudo', 'systemctl', 'disable', service_name], capture_output=True)
        subprocess.run(['sudo', 'systemctl', 'reset-failed'], capture_output=True)
        subprocess.run(['sudo', 'rm', '-f', service_file], capture_output=True)
        display_checkmark(f"\033[93mStopped and removed {service_name} service.\033[0m")

        
def ipv4_kharej():
    display_notification("\033[93mConfiguring \033[92mKharej IPV4\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/pingtunnel"):
        install_pingtunnel()
    ignore()
    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))
    local_ports = []

    for i in range(num_configs):
        local_port = input(f"\033[93mEnter \033[96mConfig Port \033[92m{i+1}\033[93m:\033[0m ")
        local_ports.append(local_port)

        stop_n_remove_service(f"kharej-pingtunnel-{i+1}")
        stop_n_remove_service(f"iran-pingtunnel-{i+1}")
        key = 16370 + i
        service_content = f'''[Unit]
Description=Pingtunnel Service {i+1}
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type server -l :{local_port} -key {key} -nolog 1 -noprint 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

        with open(f'/etc/systemd/system/kharej-pingtunnel-{i+1}.service', 'w') as file:
            file.write(service_content)

        subprocess.run('systemctl daemon-reload', shell=True)
        subprocess.run(f'sudo systemctl enable kharej-pingtunnel-{i+1}', shell=True)
        subprocess.run(f'sudo chmod u+x /etc/systemd/system/kharej-pingtunnel-{i+1}.service', shell=True)
        subprocess.run(f'sudo systemctl restart kharej-pingtunnel-{i+1}', shell=True)

    display_checkmark("\033[92mConfiguration completed!\033[0m")



def ipv6_kharej():
    display_notification("\033[93mConfiguring \033[92mKharej IPV6\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/pingtunnel"):
        install_pingtunnel()
    ignore()
    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))
    local_ports = []

    for i in range(num_configs):
        local_port = input(f"\033[93mEnter \033[96mConfig Port \033[92m{i+1}\033[93m:\033[0m ")
        local_ports.append(local_port)

        stop_n_remove_service(f"kharej-pingtunnel-{i+1}")
        stop_n_remove_service(f"iran-pingtunnel-{i+1}")
        key = 16370 + i
        service_content = f'''[Unit]
Description=Pingtunnel Service {i+1}
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type server -l :{local_port} -key {key} -noprint 1 -nolog 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

        with open(f'/etc/systemd/system/kharej-pingtunnel-{i+1}.service', 'w') as file:
            file.write(service_content)

        subprocess.run('systemctl daemon-reload', shell=True)
        subprocess.run(f'sudo systemctl enable kharej-pingtunnel-{i+1}', shell=True)
        subprocess.run(f'sudo chmod u+x /etc/systemd/system/kharej-pingtunnel-{i+1}.service', shell=True)
        subprocess.run(f'sudo systemctl restart kharej-pingtunnel-{i+1}', shell=True)

    display_checkmark("\033[92mConfiguration completed!\033[0m")
        
def iran_ping():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mIRAN\033[93m PingTunnel Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    display_notification("\033[92mTCP OPTIONS:\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    print('1. \033[93mIPV4 \033[92mTCP \033[0m')
    print('2. \033[96mIPV6 \033[92mTCP \033[0m')
    print('\033[93m─────────────────────────── \033[0m')
    display_notification("\033[92mUDP OPTIONS:\033[0m")
    print("\033[93m───────────────────────────\033[0m")
    print('3. \033[93mIPV4 \033[92mUDP \033[0m')
    print('4. \033[96mIPV6 \033[92mUDP \033[0m')
    print('5. \033[94mBack to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            tcp_ipv4_iran()
            break
        elif server_type == '2':
            tcp_ipv6_iran()
            break
        elif server_type == '3':
            udp_ipv4_iran()
            break
        elif server_type == '4':
            udp_ipv6_iran()
            break
        elif server_type == '5':
            os.system("clear")
            pingtunnel_menu()
            break
        else:
            print('Invalid choice.') 

def udp_ipv4_iran():
    display_notification("\033[93mConfiguring \033[96mIRAN \033[92mIPV6 UDP\033[93m ...\033[0m")
    if not os.path.exists("/root/pingtunnel"):
        install_pingtunnel()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    ignore()
    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))
    i = 0 
    
    if num_configs == 1:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_port = input("\033[93mEnter \033[92mKharej Config\033[93m port:\033[0m ")
        local_port = input("\033[93mEnter \033[92mlocal port\033[93m (default: 443) - \033[96m[This is your New port]\033[93m:\033[0m ") or '443'
        stop_n_remove_service("kharej-pingtunnel-1")
        stop_n_remove_service("iran-pingtunnel-1")
        key = 16370 + i

        service_content = f'''[Unit]
Description=Pingtunnel Service 1
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{local_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -key {key} -noprint 1 -nolog 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

        with open(f'/etc/systemd/system/iran-pingtunnel-1.service', 'w') as file:
            file.write(service_content)

        subprocess.run('systemctl daemon-reload', shell=True)
        subprocess.run('sudo systemctl enable iran-pingtunnel-1', shell=True)
        subprocess.run('sudo chmod u+x /etc/systemd/system/iran-pingtunnel-1.service', shell=True)
        subprocess.run('sudo systemctl restart iran-pingtunnel-1', shell=True)
        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {local_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
    else:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_ports = []

        for i in range(num_configs):
            server_port = input(f"\033[93mEnter \033[92mKharej port\033[93m for \033[96mConfig {i+1}\033[93m:\033[0m ")
            server_ports.append(server_port)


            stop_n_remove_service(f"kharej-pingtunnel-{i+1}")
            stop_n_remove_service(f"iran-pingtunnel-{i+1}")
            key = 16370 + num_configs - 1
            service_content = f'''[Unit]
Description=Pingtunnel Service {i+1}
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{server_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -key {key}  -noprint 1 -nolog 1 

[Install]
WantedBy=multi-user.target
'''

            with open(f'/etc/systemd/system/iran-pingtunnel-{i+1}.service', 'w') as file:
                file.write(service_content)

            subprocess.run('systemctl daemon-reload', shell=True)
            subprocess.run(f'sudo systemctl enable iran-pingtunnel-{i+1}', shell=True)
            subprocess.run(f'sudo chmod u+x /etc/systemd/system/iran-pingtunnel-{i+1}.service', shell=True)
            subprocess.run(f'sudo systemctl restart iran-pingtunnel-{i+1}', shell=True)

        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            for i in range(num_configs):
                print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
        return server_ports


def udp_ipv6_iran():
    display_notification("\033[93mConfiguring \033[96mIRAN \033[92mIPV6 UDP\033[93m ...\033[0m")
    if not os.path.exists("/root/pingtunnel"):
        install_pingtunnel()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    ignore()
    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))
    i = 0 
    
    if num_configs == 1:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_subdomain2 = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m: \033[0m")
        server_port = input("\033[93mEnter \033[92mKharej Config\033[93m port:\033[0m ")
        local_port = input("\033[93mEnter \033[92mlocal port\033[93m (default: 443) - \033[96m[This is your New port]\033[93m:\033[0m ") or '443'
        stop_n_remove_service("kharej-pingtunnel-1")
        stop_n_remove_service("iran-pingtunnel-1")
        key = 16370 + i

        service_content = f'''[Unit]
Description=Pingtunnel Service 1
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{local_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -key {key} -noprint 1 -nolog 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

        with open(f'/etc/systemd/system/iran-pingtunnel-1.service', 'w') as file:
            file.write(service_content)

        subprocess.run('systemctl daemon-reload', shell=True)
        subprocess.run('sudo systemctl enable iran-pingtunnel-1', shell=True)
        subprocess.run('sudo chmod u+x /etc/systemd/system/iran-pingtunnel-1.service', shell=True)
        subprocess.run('sudo systemctl restart iran-pingtunnel-1', shell=True)
        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {local_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
    else:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_subdomain2 = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m: \033[0m")

        server_ports = []

        for i in range(num_configs):
            server_port = input(f"\033[93mEnter \033[92mKharej port\033[93m for \033[96mConfig {i+1}\033[93m:\033[0m ")
            server_ports.append(server_port)


            stop_n_remove_service(f"kharej-pingtunnel-{i+1}")
            stop_n_remove_service(f"iran-pingtunnel-{i+1}")
            key = 16370 + num_configs - 1
            service_content = f'''[Unit]
Description=Pingtunnel Service {i+1}
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{server_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -key {key} -noprint 1 -nolog 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

            with open(f'/etc/systemd/system/iran-pingtunnel-{i+1}.service', 'w') as file:
                file.write(service_content)

            subprocess.run('systemctl daemon-reload', shell=True)
            subprocess.run(f'sudo systemctl enable iran-pingtunnel-{i+1}', shell=True)
            subprocess.run('sudo chmod u+x /etc/systemd/system/iran-pingtunnel-{i+1}.service', shell=True)
            subprocess.run(f'sudo systemctl restart iran-pingtunnel-{i+1}', shell=True)

        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            for i in range(num_configs):
                print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
        return server_ports
	
			
def tcp_ipv4_iran():
    display_notification("\033[93mConfiguring \033[96mIRAN \033[92mIPV4 TCP\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/pingtunnel"):
        install_pingtunnel()
    ignore()
    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))
    i = 0  

    if num_configs == 1:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_port = input("\033[93mEnter \033[92mKharej Config\033[93m port:\033[0m ")
        local_port = input("\033[93mEnter \033[92mlocal port\033[93m (default: 443) - \033[96m[This is your New port]\033[93m:\033[0m ") or '443'
        stop_n_remove_service("kharej-pingtunnel-1")
        stop_n_remove_service("iran-pingtunnel-1")
        key = 16370 + i

        service_content = f'''[Unit]
Description=Pingtunnel Service 1
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{local_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -tcp 1 -key {key} -noprint 1 -nolog 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

        with open(f'/etc/systemd/system/iran-pingtunnel-1.service', 'w') as file:
            file.write(service_content)

        subprocess.run('systemctl daemon-reload', shell=True)
        subprocess.run('sudo systemctl enable iran-pingtunnel-1', shell=True)
        subprocess.run('sudo chmod u+x /etc/systemd/system/iran-pingtunnel-1.service', shell=True)
        subprocess.run('sudo systemctl restart iran-pingtunnel-1', shell=True)
        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {local_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
    else:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_ports = []

        for i in range(num_configs):
            server_port = input(f"\033[93mEnter \033[92mKharej port\033[93m for \033[96mConfig {i+1}\033[93m:\033[0m ")
            server_ports.append(server_port)

            stop_n_remove_service(f"kharej-pingtunnel-{i+1}")
            stop_n_remove_service(f"iran-pingtunnel-{i+1}")
            key = 16370 + num_configs - 1
            service_content = f'''[Unit]
Description=Pingtunnel Service {i+1}
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{server_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -tcp 1 -key {key} -noprint 1 -nolog 1 -tcp_mw 3000
Restart=always

[Install]
WantedBy=multi-user.target
'''

            with open(f'/etc/systemd/system/iran-pingtunnel-{i+1}.service', 'w') as file:
                file.write(service_content)

            subprocess.run('systemctl daemon-reload', shell=True)
            subprocess.run(f'sudo systemctl enable iran-pingtunnel-{i+1}', shell=True)
            subprocess.run(f'sudo chmod u+x /etc/systemd/system/iran-pingtunnel-{i+1}.service', shell=True)
            subprocess.run(f'sudo systemctl restart iran-pingtunnel-{i+1}', shell=True)

        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            for i in range(num_configs):
                print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
        return server_ports


def tcp_ipv6_iran():
    display_notification("\033[93mConfiguring \033[96mIRAN \033[92mIPV6 TCP\033[93m ...\033[0m")
    if not os.path.exists("/root/pingtunnel"):
        install_pingtunnel()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    ignore()
    subprocess.run(["sudo", "sysctl", "-w", "net.core.rmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["sudo", "sysctl", "-w", "net.core.wmem_max=2500000"], stderr=subprocess.DEVNULL, check=True)
    num_configs = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mconfigurations\033[93m:\033[0m "))
    i = 0 
    if num_configs == 1:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_subdomain2 = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m: \033[0m")
        server_port = input("\033[93mEnter \033[92mKharej Config\033[93m port:\033[0m ")
        local_port = input("\033[93mEnter \033[92mlocal port\033[93m (default: 443) - \033[96m[This is your New port]\033[93m:\033[0m ") or '443'
        stop_n_remove_service("kharej-pingtunnel-1")
        stop_n_remove_service("iran-pingtunnel-1")
        key = 16370 + i

        service_content = f'''[Unit]
Description=Pingtunnel Service 1
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{local_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -tcp 1 -key {key} -noprint 1 -nolog 1 
Restart=always

[Install]
WantedBy=multi-user.target
'''

        with open(f'/etc/systemd/system/iran-pingtunnel-1.service', 'w') as file:
            file.write(service_content)

        subprocess.run('systemctl daemon-reload', shell=True)
        subprocess.run('sudo systemctl enable iran-pingtunnel-1', shell=True)
        subprocess.run('sudo chmod u+x /etc/systemd/system/iran-pingtunnel-1.service', shell=True)
        subprocess.run('sudo systemctl restart iran-pingtunnel-1', shell=True)
        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            print(f"\033[93m| Your Address & Port: {current_ipv4} : {local_port}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
    else:
        server_subdomain = input("\033[93mEnter \033[92mKharej\033[93m IPV4:\033[0m ")
        server_subdomain2 = input("\033[93mEnter \033[92mKharej\033[96m IPV6\033[93m: \033[0m")

        server_ports = []

        for i in range(num_configs):
            server_port = input(f"\033[93mEnter \033[92mKharej port\033[93m for \033[96mConfig {i+1}\033[93m:\033[0m ")
            server_ports.append(server_port)


            stop_n_remove_service(f"kharej-pingtunnel-{i+1}")
            stop_n_remove_service(f"iran-pingtunnel-{i+1}")
            key = 16370 + num_configs - 1
            service_content = f'''[Unit]
Description=Pingtunnel Service {i+1}
After=network.target

[Service]
ExecStart=/root/./pingtunnel -type client -tcp_mw 3000 -l :{server_port} -s {server_subdomain} -t {server_subdomain}:{server_port} -tcp 1 -key {key} -noprint 1 -nolog 1 -tcp_mw 3000

[Install]
WantedBy=multi-user.target
'''

            with open(f'/etc/systemd/system/iran-pingtunnel-{i+1}.service', 'w') as file:
                file.write(service_content)

            subprocess.run('systemctl daemon-reload', shell=True)
            subprocess.run(f'sudo systemctl enable iran-pingtunnel-{i+1}', shell=True)
            subprocess.run(f'sudo chmod u+x /etc/systemd/system/iran-pingtunnel-{i+1}.service', shell=True)
            subprocess.run(f'sudo systemctl restart iran-pingtunnel-{i+1}', shell=True)

        display_checkmark("\033[92mConfiguration completed!\033[0m")
        current_ipv4 = get_ipv4()

        if current_ipv4:
            print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
            for i in range(num_configs):
                print(f"\033[93m| Config {i+1} - Your Address & Port: {current_ipv4} : {server_ports[i]}  \033[0m")
            print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
        else:
            display_error("\033[91mUnable to retrieve server's IPv4 address.\033[0m")
        return server_ports
		
def icmp_socat_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIcmptunnel Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[96mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            start_ic_kharej()
            break
        elif server_type == '2':
            start_ic_iran()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def icmp_choose():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mSocat Single config \033[0m')
    print('2. \033[96mHaproxy Mutli config\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            icmp_port_forwarding()
            break
        elif server_type == '2':
            haproxy_icmp()
            break
        else:
            print('Invalid choice.')

def icmp_port_forwarding():
    while True:
        print("\033[93m╭───────────────────────────────────────╮\033[0m")
        display_notification("\033[93mPort Forwarding Options\033[93m:\033[0m")
        print("1. \033[92mTCP\033[0m")
        print("2. \033[96mUDP\033[0m")
        print("\033[93m╰───────────────────────────────────────╯\033[0m")
        port_forward_choice = input("Enter your choice (1 or 2): ")

        if port_forward_choice == "1":
            display_notification("\033[93mConfiguring \033[92mTCP\033[93m ...\033[0m")
            print("\033[93m──────────────────────────────────────────────────\033[0m")
            local_port_range = input("\033[93mEnter \033[92mlocal\033[93m port (default: 443): \033[0m") or "443"
            remote_port = input("\033[93mEnter \033[92mKharej \033[96mConfig\033[93m port:\033[0m ")
            socat_command = f"TCP-LISTEN:{local_port_range},fork TCP:70.0.0.1:{remote_port}"
            break
        elif port_forward_choice == "2":
            display_notification("\033[93mConfiguring \033[92mUDP\033[93m ...\033[0m")
            print("\033[93m──────────────────────────────────────────────────\033[0m")
            local_port_range = input("\033[93mEnter \033[92mlocal\033[93m port (default: 443): \033[0m") or "443"
            remote_port = input("\033[93mEnter \033[92mKharej \033[96mConfig\033[93m port:\033[0m ")
            socat_command = f"UDP-LISTEN:{local_port_range},fork UDP:70.0.0.1:{remote_port}"
            break
        else:
            print("Invalid choice. Please try again.")

    socat_service_content = f"""
[Unit]
Description=Port Forwarding {port_forward_choice}

[Service]
ExecStart=/usr/bin/socat {socat_command}
Restart=always

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/portforwarding.service", "w") as f:
        f.write(socat_service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo systemctl enable portforwarding")
    os.system("sudo chmod u+x /etc/systemd/system/portforwarding.service")
    os.system("sudo systemctl restart portforwarding")
    display_checkmark("\033[92mPortforward Completed successfully!\033[0m")

    current_ipv4 = get_ipv4()
    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Address & Port: {current_ipv4} : {local_port_range}  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
def restart_haproxy():
    os.system("systemctl restart haproxy")
    display_checkmark("\033[92mHAProxy service restarted!\033[0m")
    
def install_haproxy():
    display_loading()
    os.system("apt-get install -y haproxy > /dev/null")
    display_checkmark("\033[92mHAProxy installation completed.!\033[0m")
    
def haproxy_icmp():
    install_haproxy()
    display_notification("\033[93mConfiguring ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    backend_count = int(input("\033[93mEnter the number of \033[92mConfigs\033[93m:\033[0m "))

    config_parts = []

    config_parts.append("global")
    config_parts.append("    log /dev/log local0")
    config_parts.append("    log /dev/log local1 notice")
    config_parts.append("    chroot /var/lib/haproxy")
    config_parts.append("    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners")
    config_parts.append("    stats timeout 30s")
    config_parts.append("    user haproxy")
    config_parts.append("    group haproxy")
    config_parts.append("    daemon")
    config_parts.append("")
    config_parts.append("# Default SSL material locations")
    config_parts.append("ca-base /etc/ssl/certs")
    config_parts.append("crt-base /etc/ssl/private")
    config_parts.append("")
    config_parts.append("# See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate")
    config_parts.append("ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE")
    config_parts.append("ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256")
    config_parts.append("ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets")
    config_parts.append("")
    config_parts.append("defaults")
    config_parts.append("    log global")
    config_parts.append("    mode tcp")
    config_parts.append("    option dontlognull")
    config_parts.append("    timeout connect 5000")
    config_parts.append("    timeout client 50000")
    config_parts.append("    timeout server 50000")
    config_parts.append("    errorfile 400 /etc/haproxy/errors/400.http")
    config_parts.append("    errorfile 403 /etc/haproxy/errors/403.http")
    config_parts.append("    errorfile 408 /etc/haproxy/errors/408.http")
    config_parts.append("    errorfile 500 /etc/haproxy/errors/500.http")
    config_parts.append("    errorfile 502 /etc/haproxy/errors/502.http")
    config_parts.append("    errorfile 503 /etc/haproxy/errors/503.http")
    config_parts.append("    errorfile 504 /etc/haproxy/errors/504.http")
    config_parts.append("")
    frontend_bind = input("\033[93mEnter \033[92mHaproxy Port\033[93m (default: *:443):\033[0m ") or "*:443"
    config_parts.append(f"frontend ip_iran")
    config_parts.append(f"    bind *:{frontend_bind} transparent")
    config_parts.append("    mode tcp")
    config_parts.append("    default_backend kharej")
    config_parts.append("")
    config_parts.append("backend kharej")
    config_parts.append("    mode tcp")

    for i in range(backend_count):
        remote_port = input(f"\033[93mEnter \033[96mKharej \033[92mConfig Port {i+1}\033[93m: \033[0m")
        config_parts.append(f"    server server{i+1} 70.0.0.1:{remote_port}")

    haproxy_config = "\n".join(config_parts)

    with open("/etc/haproxy/haproxy.cfg", "w") as cfg_file:
        cfg_file.write(haproxy_config)

    restart_haproxy()
    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Address & Port: {current_ipv4} : {frontend_bind}  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return haproxy_config
    

def start_ic_kharej():
    display_notification("\033[93mConfiguring \033[92mKharej\033[93m ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()

    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    if os.path.exists("/etc/icmp.sh"):
        os.remove("/etc/icmp.sh")

    with open("/etc/icmp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/root/icmptunnel/icmptunnel -s -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.1 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp.sh\n"
    with open("/etc/cron.d/icmp-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")

def start_ic_iran():
    display_notification("\033[93mConfiguring \033[92mIRAN \033[93m...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.chdir("/root/icmptunnel")

    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address:\033[0m ")

    if os.path.exists("/etc/icmp-iran.sh"):
        os.remove("/etc/icmp-iran.sh")

    with open("/etc/icmp-iran.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"/root/icmptunnel/icmptunnel {server_ipv4} -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.2 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp-iran.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp-iran.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp-iran.sh\n"
    with open("/etc/cron.d/icmp-iran", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    icmp_choose()
        
		
def hans_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mHans Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[96mIRAN \033[0m')
    print('3. \033[94mBack to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hns_icmp_kharej()
            break
        elif server_type == '2':
            hns_icmp_iran()
            break
        elif server_type == '3':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def hans_choose():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mSocat Single config \033[0m')
    print('2. \033[96mHaproxy Mutli config\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            hans_port_forwarding()
            break
        elif server_type == '2':
            haproxy_hans()
            break
        else:
            print('Invalid choice.')

def hans_port_forwarding():

    while True:
        print("\033[93m╭───────────────────────────────────────╮\033[0m")
        display_notification("\033[93mPort Forwarding Options\033[93m:\033[0m")
        print("1. \033[92mTCP\033[0m")
        print("2. \033[96mUDP\033[0m")
        print("\033[93m╰───────────────────────────────────────╯\033[0m")
        port_forward_choice = input("Enter your choice (1 or 2): ")

        if port_forward_choice == "1":
            display_notification("\033[93mConfiguring \033[92mTCP\033[93m ...\033[0m")
            print("\033[93m──────────────────────────────────────────────────\033[0m")
            local_port_range = input("\033[93mEnter \033[92mlocal\033[93m port (default: 443): \033[0m") or "443"
            remote_port = input("\033[93mEnter \033[92mKharej \033[96mConfig\033[93m port:\033[0m ")
            socat_command = f"TCP-LISTEN:{local_port_range},fork TCP:80.1.2.1:{remote_port}"
            break
        elif port_forward_choice == "2":
            display_notification("\033[93mConfiguring \033[92mUDP\033[93m ...\033[0m")
            print("\033[93m──────────────────────────────────────────────────\033[0m")
            local_port_range = input("\033[93mEnter \033[92mlocal\033[93m port (default: 443): \033[0m") or "443"
            remote_port = input("\033[93mEnter \033[92mKharej \033[96mConfig\033[93m port:\033[0m ")
            socat_command = f"UDP-LISTEN:{local_port_range},fork UDP:80.1.2.1:{remote_port}"
            break
        else:
            print("Invalid choice. Please try again.")

    socat_service_content = f"""
[Unit]
Description=Port Forwarding {port_forward_choice}

[Service]
ExecStart=/usr/bin/socat {socat_command}
Restart=always

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/portforwarding.service", "w") as f:
        f.write(socat_service_content)

    os.system("systemctl daemon-reload")
    os.system("sudo systemctl enable portforwarding")
    os.system("sudo chmod u+x /etc/systemd/system/portforwarding.service")
    os.system("sudo systemctl restart portforwarding")
    display_checkmark("\033[92mPortforward Completed successfully!\033[0m")

    current_ipv4 = get_ipv4()
    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Address & Port: {current_ipv4} : {local_port_range}  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
def haproxy_hans():
    install_haproxy()
    display_notification("\033[93mConfiguring ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    backend_count = int(input("\033[93mEnter the number of \033[92mConfigs\033[93m:\033[0m "))

    config_parts = []

    config_parts.append("global")
    config_parts.append("    log /dev/log local0")
    config_parts.append("    log /dev/log local1 notice")
    config_parts.append("    chroot /var/lib/haproxy")
    config_parts.append("    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners")
    config_parts.append("    stats timeout 30s")
    config_parts.append("    user haproxy")
    config_parts.append("    group haproxy")
    config_parts.append("    daemon")
    config_parts.append("")
    config_parts.append("# Default SSL material locations")
    config_parts.append("ca-base /etc/ssl/certs")
    config_parts.append("crt-base /etc/ssl/private")
    config_parts.append("")
    config_parts.append("# See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate")
    config_parts.append("ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE")
    config_parts.append("ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256")
    config_parts.append("ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets")
    config_parts.append("")
    config_parts.append("defaults")
    config_parts.append("    log global")
    config_parts.append("    mode tcp")
    config_parts.append("    option dontlognull")
    config_parts.append("    timeout connect 5000")
    config_parts.append("    timeout client 50000")
    config_parts.append("    timeout server 50000")
    config_parts.append("    errorfile 400 /etc/haproxy/errors/400.http")
    config_parts.append("    errorfile 403 /etc/haproxy/errors/403.http")
    config_parts.append("    errorfile 408 /etc/haproxy/errors/408.http")
    config_parts.append("    errorfile 500 /etc/haproxy/errors/500.http")
    config_parts.append("    errorfile 502 /etc/haproxy/errors/502.http")
    config_parts.append("    errorfile 503 /etc/haproxy/errors/503.http")
    config_parts.append("    errorfile 504 /etc/haproxy/errors/504.http")
    config_parts.append("")
    frontend_bind = input("\033[93mEnter \033[92mHaproxy Port\033[93m (default: 443):\033[0m ") or "*:443"
    config_parts.append(f"frontend ip_iran")
    config_parts.append(f"    bind *:{frontend_bind} transparent")
    config_parts.append("    mode tcp")
    config_parts.append("    default_backend kharej")
    config_parts.append("")
    config_parts.append("backend kharej")
    config_parts.append("    mode tcp")

    for i in range(backend_count):
        remote_port = input(f"\033[93mEnter \033[96mKharej \033[92mConfig Port {i+1}\033[93m: \033[0m")
        config_parts.append(f"    server server{i+1} 80.1.2.1:{remote_port}")

    haproxy_config = "\n".join(config_parts)

    with open("/etc/haproxy/haproxy.cfg", "w") as cfg_file:
        cfg_file.write(haproxy_config)

    restart_haproxy() 
    current_ipv4 = get_ipv4()

    if current_ipv4:
        print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
        print(f"\033[93m| Your Address & Port: {current_ipv4} : {frontend_bind}  \033[0m")
        print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    return haproxy_config    



def hns_icmp_kharej():
    display_notification("\033[93mConfiguring Kharej ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/hans-1.1"):
        hanss_install_menu()
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    hans_directory = "/root/hans-1.1"

    os.chdir(hans_directory)
    os.system(f"./hans -s 80.1.2.0 -p azumi86chwan -d icmp")

    subprocess.call(["crontab", "-r", "-u", "root"])

    hans_kharej_command = f"{hans_directory}/hans -s 80.1.2.0 -p azumi86chwan -d icmp"
    subprocess.run(["sed", "-i", f"/{hans_kharej_command}/d", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)

    if os.path.exists("/etc/hans.sh"):
        os.remove("/etc/hans.sh")

    with open("/etc/hans.sh", "w") as f:
        f.write(f"{hans_kharej_command}\n")

    subprocess.run(["chmod", "700", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    cron_job_command = f"@reboot /bin/bash /etc/hans.sh\n"
    with open("/etc/cron.d/hans-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/hans-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
	
def hns_icmp_iran():
    display_notification("\033[93mConfiguring IRAN ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    if not os.path.exists("/root/hans-1.1"):
        hanss_install_menu()
    subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/icmp_echo_ignore_all"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")

    os.chdir("/root/hans-1.1")
    os.system(f"./hans -c {server_ipv4} -p azumi86chwan -d icmp")

    os.system("ping -c 4 80.1.2.1")

    subprocess.call(["rm", "-f", "/etc/cron.d/hans"])

    hans_command = f"/root/hans-1.1/hans -c {server_ipv4} -p azumi86chwan -d icmp"
    subprocess.run(["sed", "-i", f"/{hans_command}/d", "/etc/hans.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=False)

    if os.path.exists("/etc/hans.sh"):
        os.remove("/etc/hans.sh")

    with open("/etc/hans.sh", "w") as f:
        f.write(f"{hans_command}\n")

    cron_job_command = f"@reboot root /bin/bash /etc/hans.sh\n"
    with open("/etc/cron.d/hans-iran", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/hans-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")
    hans_choose()

main_menu()
