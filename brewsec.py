from cli.menu import clear_cli, header, menu, get_lab_choice, Colors
from options.sql_injection import sql_injection
from options.access_control import access_control
from options.cross_site_scripting import cross_site_scripting
from options.cross_site_request_forgery import cross_site_request_forgery
from options.cache_poisoning import cache_poisoning
from core.lab_launcher import start_secure_application

LABS = {
    "1": sql_injection,
    "2": access_control,
    "3": cross_site_scripting,
    "4": cross_site_request_forgery,
    "5": cache_poisoning
}

def main():
    clear_cli()
    header()
    
    while True:
        menu()
        
        choice = get_lab_choice()

        if choice == "0":
            clear_cli()
            print(
                f"\n{Colors.CYAN}[+]{Colors.RESET} Running Secure Application...\n"
            )
            start_secure_application("secure")

        
        if choice == "q":
            clear_cli()
            print(
                f"\n{Colors.CYAN}[+]{Colors.RESET} Goodbye! :)\n"
            )
            break
        
        lab = LABS.get(choice)
        
        if lab:
            clear_cli()
            header()
            
            lab()
            
            print(f"\n{Colors.CYAN}[+]{Colors.RESET} Lab ended. Press Enter to return to menu...")
            input()
            
            clear_cli()
            header()
            
        else:
            print(
                f"{Colors.RED}[!]{Colors.RESET} Invalid choice!"
            )

if __name__ == "__main__":
    main()