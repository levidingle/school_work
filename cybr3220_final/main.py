# =============================================================================
# CYBR3220 Final Project - CyberSec Toolkit
# Entry point: displays the main menu and dispatches to defense/offense modules
# =============================================================================

from defense import port_scanner, file_integrity, log_analyzer
from defense import password_checker, process_monitor, virustotal_lookup, firewall_audit
from offense import distration, dns_enum, keylogger, hash_cracker
from utils.helpers import print_banner, print_blue_banner, print_red_banner, print_section, pause


def defense_menu():
    while True:
        print_blue_banner()
        print_section("BLUE TEAM - Cyber Defense")
        print("  [1]  Port Scanner")
        print("  [2]  File Integrity Monitor")
        print("  [3]  Log Analyzer")
        print("  [4]  Password Strength Checker")
        print("  [5]  Suspicious Process Monitor")
        print("  [6]  VirusTotal File Hash Lookup")
        print("  [7]  Firewall Rule Auditor")
        print("  [0]  Back")

        choice = input("\nSelect a tool: ").strip()
        if choice == "1":
            port_scanner.run();     pause()
        elif choice == "2":
            file_integrity.run();   pause()
        elif choice == "3":
            log_analyzer.run();     pause()
        elif choice == "4":
            password_checker.run(); pause()
        elif choice == "5":
            process_monitor.run();  pause()
        elif choice == "6":
            virustotal_lookup.run(); pause()
        elif choice == "7":
            firewall_audit.run();   pause()
        elif choice == "0":
            return
        else:
            print("[-] Invalid option.")
            pause()


def offense_menu():
    while True:
        print_red_banner()
        print_section("RED TEAM - Penetration Testing")
        print("  [1]  Distraction")
        print("  [2]  DNS Enumerator")
        print("  [3]  Keylogger")
        print("  [4]  Hash Cracker")
        print("  [0]  Back")

        choice = input("\nSelect a tool: ").strip()
        if choice == "1":
            distration.run();    pause()
        elif choice == "2":
            dns_enum.run();      pause()
        elif choice == "3":
            keylogger.run();     pause()
        elif choice == "4":
            hash_cracker.run();  pause()
        elif choice == "0":
            return
        else:
            print("[-] Invalid option.")
            pause()


def main():
    while True:
        print_banner()
        print("  [1]  Blue Team  - Cyber Defense")
        print("  [2]  Red Team   - Offensive Tools")
        print("  [0]  Exit")

        choice = input("\nSelect a category: ").strip()
        if choice == "1":
            defense_menu()
        elif choice == "2":
            offense_menu()
        elif choice == "0":
            print("\n[*] Exiting. Stay secure.\n")
            break
        else:
            print("[-] Invalid option. Try again.")


if __name__ == "__main__":
    main()
