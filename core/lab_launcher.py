import importlib
from cli.menu import Colors

LAB_PORTS = {
    ("sql_injection", "level_01"): 3001,
    ("sql_injection", "level_02"): 3002,
    ("sql_injection", "level_03"): 3003,
    ("sql_injection", "level_04"): 3004,
    ("sql_injection", "level_05"): 3005,
}

def launch_lab(category, level):
    module_name = f"labs.{category}.{level}.app"
    
    print(f"{Colors.CYAN}[+]{Colors.RESET} Loading {category} {level}...")
    
    module = importlib.import_module(module_name)
    
    app = module.create_app()
    
    port = LAB_PORTS.get((category, level))
    
    if port is None:
        print(f"{Colors.RED}[!]{Colors.RESET} No port configured for this lab.")
        return
    
    print(f"{Colors.CYAN}[+]{Colors.RESET} Starting Flask application on port {port}...")
    
    app.run(
        host="127.0.0.1",
        port=port,
        debug=True,
        use_reloader=False
    )