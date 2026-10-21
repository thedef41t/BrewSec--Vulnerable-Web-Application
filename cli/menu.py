import os

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

def clear_cli():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print(
        f"""
        {Colors.CYAN}=================================================
        ____                     ____            
        | __ ) _ __ _____      __/ ___|  ___  ___ 
        |  _ \\| '__/ _ \\ \\ /\\ / /\\___ \\ / _ \\/ __|
        | |_) | | |  __/\\ V  V /  ___) |  __/ (__
        |____/|_|  \\___| \\_/\\_/  |____/ \\___|\\___|
                {Colors.BOLD}{Colors.WHITE}Vulnerable Web Application{Colors.RESET}
                                    {Colors.BOLD}{Colors.WHITE}by: def41t{Colors.RESET}
        {Colors.CYAN}================================================={Colors.RESET}
        """
    )

def menu():
    print(
        f"""
        {Colors.GREEN}[1]{Colors.RESET} SQL Injection {Colors.GRAY}(SQLi){Colors.RESET}
        {Colors.GREEN}[2]{Colors.RESET} Access Control Vulnerability
        {Colors.GREEN}[3]{Colors.RESET} Cross-Site Scripting {Colors.GRAY}(XSS){Colors.RESET}

        {Colors.RED}[q]{Colors.RESET} Quit
        """
    )

def get_lab_choice():
    return input(
        f"{Colors.CYAN}[?]{Colors.RESET} Select an option: "
    ).strip().lower()

def get_level_choice():
    return input(
        f"{Colors.CYAN}[?]{Colors.RESET} Select a level: "
    ).strip().lower()