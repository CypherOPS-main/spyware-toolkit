import json
import os
import subprocess


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


def setup_winget():
    print("Installing WinGet...")
    # TODO


def check_winget():
    if os_type == "Windows":
        try:
            subprocess.run(
                ["winget", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return True
        except:
            # implement winget install logic? setup_winget()
            print("Failed to install WinGet. Please install it manually.")
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
            print("pipx installed successfully!")
            return True
        except:
            print("Failed to install pipx. Please install it manually.")
            exit(1)


def list_programs(programs_data):
    print("List of available programs:")
    for program in programs_data:
        print(f"{program['name']} - {program['description']}")
        print()


def install_programs(programs_data):
    print("Starting Installation!")
    for program in programs_data:
        install_info = program[os_type.lower()]
        print(f"Installing {program['name']}...")

        if os_type == "Windows":
            if "winget" in install_info:
                app_name = install_info["winget"]
                print(f"winget install -e --source winget {app_name}")
                # subprocess.run(
                #     "winget", "install", "-e", "--source", "winget", app_name
                # )
            else:
                print(
                    "Skipping installation of this program as it is not available on WinGet."
                )

        elif os_type == "Linux":
            if install_info["package_manager"]:
                package_manager = install_info["package_manager"]
                if package_manager == manager.lower():
                    install_command = install_info["install_command"]
                    # subprocess.run([package_manager, install_command], shell=True)
                    print(f"{package_manager} {install_command}")
            else:
                install_command = install_info["install_command"]
                # subprocess.run([install_command], shell=True)
                print(install_command)

        elif os_type == "Windows" or os_type == "Linux" and "pipx" in install_info:
            if check_pipx():
                app_name = install_info["pipx"]
                # subprocess.run(["pipx", "install", app_name])
                print(f"pipx install {app_name}")

        print(f"{program['name']} installed successfully!")
        print()


def main():
    if os_type == "Windows" or os_type == "Linux":
        print(
            f"Welcome to the installer! What Would you like to install? (OS: {os_type})"
        )

    while True:
        try:
            with open("list.json") as json_file:
                programs_data = json.load(json_file)["programs"]
        except FileNotFoundError:
            print(
                "Could not find list.json. Please run the program in the same directory as list.json."
            )
            exit(1)

        print("1. Install the programs")
        print("2. List the programs")
        print("3. Exit the installer")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                install_programs(programs_data)
            elif choice == 2:
                list_programs(programs_data)
            elif choice == 3:
                print("Exiting the installer...")
                exit(1)
        except ValueError:
            print("Please enter a valid choice.")
            print()


if __name__ == "__main__":
    main()