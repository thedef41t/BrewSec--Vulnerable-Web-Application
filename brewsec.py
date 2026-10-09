from cli.menu import clear_cli, header, menu, get_lab_choice, Colors
from options.sql_injection import sql_injection

LABS = {
    "1": sql_injection,
}

def main():
    clear_cli()
    header()
    
    while True:
        menu()
        
        choice = get_lab_choice()
        
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