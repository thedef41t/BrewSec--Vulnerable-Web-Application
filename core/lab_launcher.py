import importlib
import traceback
from cli.menu import Colors

LAB_PORTS = {
    ("sql_injection", "level_01"): 3001,
    ("sql_injection", "level_02"): 3002,
    ("sql_injection", "level_03"): 3003,
    ("sql_injection", "level_04"): 3004,
    ("sql_injection", "level_05"): 3005,
}


def launch_lab(category, level):
    try:
        module_name = f"labs.{category}.{level}.app"

        print(f"{Colors.CYAN}[+]{Colors.RESET} Importing: {module_name}", flush=True)
        module = importlib.import_module(module_name)

        print(f"{Colors.CYAN}[+]{Colors.RESET} Creating Flask app...", flush=True)
        app = module.create_app()

        port = LAB_PORTS.get((category, level))

        if port is None:
            print(f"{Colors.RED}[!]{Colors.RESET} No port configured for {category} {level}")
            return

        print(
            f"{Colors.CYAN}[+]{Colors.RESET} Starting server at http://127.0.0.1:{port}",
            flush=True,
        )

        app.run(
            host="127.0.0.1",
            port=port,
            debug=False,
            use_reloader=False,
        )

        print(f"{Colors.YELLOW}[!]{Colors.CYAN} Flask server stopped.", flush=True)

    except Exception:
        traceback.print_exc()
        input("Press Enter to continue...")