from cli.menu import Colors, get_level_choice
from core.lab_launcher import launch_lab

def sql_injection():
    print(
        f"""
        {Colors.GREEN}[1]{Colors.RESET} Level 01 - Basic SQL Injection {Colors.GRAY}(Retrieve a hidden data){Colors.RESET}
        {Colors.GREEN}[2]{Colors.RESET} Level 02 - SQL Injection {Colors.GRAY}(Login bypass){Colors.RESET}
        {Colors.GREEN}[3]{Colors.RESET} Level 03 - SQL Injection {Colors.GRAY}(UNION attack){Colors.RESET}
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
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting SQL Injection Level 01...")
    launch_lab("sql_injection", "level_01")


def start_level_02():
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting SQL Injection Level 02...")
    launch_lab("sql_injection", "level_02")

def start_level_03():
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting SQL Injection Level 03...")
    launch_lab("sql_injection", "level_03")