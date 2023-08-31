#!/usr/bin/python3
# 42

import json
import os
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

def print_colored(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

def print_success(text):
    print_colored(text, Fore.GREEN)

def print_error(text):
    print_colored(text, Fore.RED)

def print_warning(text):
    print_colored(text, Fore.YELLOW)

def print_info(text):
    print_colored(text, Fore.CYAN)

def check_os():
    if os.name == "nt":
        return "Windows"
    elif os.name == "posix":
        return "Linux"
    else:
        return "Unknown"


def check_linux_package_manager():
    if os.path.exists("/usr/bin/apt"):
        return "apt"
    elif os.path.exists("/usr/bin/pacman"):
        return "pacman"
    elif os.path.exists("/usr/bin/dnf"):
        return "dnf"
    elif os.path.exists("/usr/bin/yum"):
        return "yum"
    else:
        return None


os_type = check_os()
manager = check_linux_package_manager()


def check_winget():
    if os_type == "Windows":
        try:
            subprocess.run(
                ["winget", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return True
        except:
            print_error("Please install WinGet before running the script!")
            exit(1)


def check_pipx():
    try:
        subprocess.run(
            ["pipx", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except:
        try:
            subprocess.run(
                ["python3", "-m", "pip", "install", "pipx"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print_success("pipx installed successfully!")
            return True
        except:
            print_error("Failed to install pipx. Please install it manually.")
            exit(1)


def install_with_pipx(app_name):
    if check_pipx():
        print(f"pipx install {app_name}")
        subprocess.run(["pipx", "install", app_name])


def list_programs(programs_data):
    print("List of available programs:")
    for program in programs_data:
        print(f"{program['name']} - {program['description']}")
    print()


def install_programs(programs_data):
    print_info("List of available programs:")
    for idx, program in enumerate(programs_data):
        print(f"{idx + 1}. {program['name']} - {program['description']}")

    selected_indices = input("Enter the indices of programs to install (e.g., 1 3 5), or type 'all' to install all: ")
    print()

    if selected_indices.lower() == 'all':
        selected_programs = programs_data
    else:
        selected_indices = [int(idx) - 1 for idx in selected_indices.split()]
        selected_programs = [programs_data[idx] for idx in selected_indices]
    
    for program in selected_programs:
        install_info = program[os_type.lower()]
        print_info(f"Installing {program['name']}...")

        if os_type == "Windows":
            if "winget" in install_info and check_winget():
                app_name = install_info["winget"]
                print(f"winget install --source winget {app_name}")
                subprocess.run(["winget", "install", "--source", "winget", app_name])
            elif "pipx" in install_info:
                install_with_pipx(install_info["pipx"])
            else:
                print_warning("Windows install instructions not found, edit the list.json file, skipping...")

        elif os_type == "Linux":
            package_manager = install_info.get("package_manager", "").lower()
            if package_manager == manager.lower():
                install_command = install_info.get("install_command", "")
                if install_command:
                    print(f"{install_command}")
                    subprocess.run([install_command], shell=True)
            elif "pipx" in install_info:
                install_with_pipx(install_info["pipx"])
            elif "install_command" in install_info:
                install_command = install_info.get("install_command", "")
                if install_command:
                    subprocess.run([install_command], shell=True)
                    print(install_command)
            else:
                print_warning("Linux install instructions not found, edit the list.json file, skipping...")
        print_success(f"{program['name']} installed successfully!")
        print()


def add_program(programs_data):
    new_program = {
        "name": input("Enter the name of the program: "),
        "description": input("Enter the description of the program: "),
        "windows": {},
        "linux": {},
    }

    os_choice = input("Enter the OS to install the program on (Windows/Linux): ")

    if os_choice.lower() == "windows":
        new_program["windows"]["winget"] = input("Enter the WinGet App ID: ")
    elif os_choice.lower() == "linux":
        new_program["linux"]["package_manager"] = input("Enter the package manager: ")
        new_program["linux"]["install_command"] = input("Enter the install command: ")
    else:
        print_error("Please enter a valid OS.")
        return
    programs_data.append(new_program)

    with open("list.json", "w") as json_file:
        json.dump({"programs": programs_data}, json_file, indent=4)
    print_success(
        "Program added successfully! Manually update the list.json file to make further changes."
    )
    print()


def main():
    if os_type == "Windows" or os_type == "Linux":
        print_success(
            f"Welcome to the installer! What Would you like to install? (OS: {os_type})"
        )
    while True:
        try:
            with open("list.json") as json_file:
                programs_data = json.load(json_file)["programs"]
        except FileNotFoundError:
            print_error(
                "Could not find list.json. Please run the program in the same directory as list.json."
            )
            exit(1)
        print("1. Install the programs")
        print("2. List the programs")
        print("3. Add a program")
        print("4. Exit the installer")

        try:
            choice = int(input("Enter your choice: "))
            print()

            if choice == 1:
                install_programs(programs_data)
            elif choice == 2:
                list_programs(programs_data)
            elif choice == 3:
                add_program(programs_data)
            elif choice == 4:
                print_error("Exiting the installer...")
                exit(1)
        except ValueError:
            print_error("Please enter a valid choice.")
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nExiting the installer...")
        exit(1)