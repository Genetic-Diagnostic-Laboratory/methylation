"""Entry point for the PyInstaller build."""

import sys

from cli import __version__
from cli.main import methyl

# (menu label, argv handed to the CLI)
MENU = [
    ("Generate reports", ["report", "run"]),
    ("Run analysis", ["analysis", "run"]),
    ("Set BWS template", ["config", "set-template", "bws"]),
    ("Set RSS template", ["config", "set-template", "rss"]),
    ("Show settings", ["config", "show"]),
]


def menu():
    """Show a numbered menu until the user exits, so double-clicking the exe is usable."""
    while True:
        print(f"\nMethylation Tools {__version__}")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"  {i}. {label}")
        print("  0. Exit")

        choice = input("\nChoice: ").strip()
        if choice == "0":
            return
        if not (choice.isdigit() and 1 <= int(choice) <= len(MENU)):
            print("Invalid choice.")
            continue

        try:
            # standalone_mode=False keeps click from exiting the whole process
            methyl.main(args=MENU[int(choice) - 1][1], standalone_mode=False)
        except SystemExit:
            # The report pipeline exits on ordinary outcomes, such as a cancelled dialog
            pass
        except Exception as e:
            print(f"Error: {e}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Double-clicking passes no arguments, so show the menu instead of the help text
    if len(sys.argv) == 1:
        menu()
    else:
        methyl()
