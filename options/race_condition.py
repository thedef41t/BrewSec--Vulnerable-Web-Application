from cli.menu import Colors, get_level_choice
from core.lab_launcher import launch_lab

def race_condition():
    print(
        f"""
        {Colors.GREEN}[1]{Colors.RESET} Level 01 - Race Condition {Colors.GRAY}(Limit Overrun){Colors.RESET}
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
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting Race Condition Level 01...")
    launch_lab("race_condition", "level_01")