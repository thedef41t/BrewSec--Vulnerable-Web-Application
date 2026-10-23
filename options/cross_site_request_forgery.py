from cli.menu import Colors, get_level_choice
from core.lab_launcher import launch_lab

def cross_site_request_forgery():
    print(
        f"""
        {Colors.GREEN}[1]{Colors.RESET} Level 01 - CSRF with no defenses
        """
    )
    
    choice = get_level_choice()
        
    if choice == "1":
        start_level_01()
        
    elif choice == "q":
        return
    
    else:
        print(f"{Colors.RED}[!]{Colors.RESET} Invalid level.")


def start_level_01():
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting Cross-Site Request Forgery Level 01...")
    launch_lab("cross_site_request_forgery", "level_01")