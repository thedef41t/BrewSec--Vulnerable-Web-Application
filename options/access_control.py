from cli.menu import Colors, get_level_choice
from core.lab_launcher import launch_lab

def access_control():
    print(
        f"""
        {Colors.GREEN}[1]{Colors.RESET} Level 01 - Horizontal Privilege Escalation {Colors.GRAY}(Basic IDOR){Colors.RESET}
        {Colors.GREEN}[2]{Colors.RESET} Level 02 - Broken Session Authorization
        {Colors.GREEN}[2]{Colors.RESET} Level 03 - Referer Based Access Control
        """
    )
    
    choice = get_level_choice()
        
    if choice == "1":
        start_level_01()
        
    elif choice == "2":
        start_level_02()

    elif choice == "3":
        start_level_03()
        
    elif choice == "q":
        return
    
    else:
        print(f"{Colors.RED}[!]{Colors.RESET} Invalid level.")


def start_level_01():
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting Access Control Level 01...")
    launch_lab("access_control", "level_01")

def start_level_02():
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting Access Control Level 02...")
    launch_lab("access_control", "level_02")

def start_level_03():
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting Access Control Level 03...")
    launch_lab("access_control", "level_03")