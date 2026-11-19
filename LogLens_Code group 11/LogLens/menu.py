"""Component 1 - Menu, input and validation (Member 1)."""
import datetime as dt

MENU = """
=========== LogLens: Server Log Analyzer ===========
 1. Load a log file            6. Save summary (JSON + CSV)
 2. Filter by level / date     7. Generate charts
 3. Search messages            8. Generate sample log file
 4. Summary and health score   0. Exit
 5. Top errors / busiest hours
===================================================="""

def show_menu():
    print(MENU)

def get_choice(valid=("0", "1", "2", "3", "4", "5", "6", "7", "8")):
    """Ask until the user enters a valid menu option."""
    while True:
        ch = input("Choose an option: ").strip()
        if ch in valid:
            return ch
        print("  Invalid choice, enter a number from 0 to 8.")

def get_level():
    """Return INFO / WARNING / ERROR, or None if the user presses Enter."""
    while True:
        lvl = input("Level (INFO/WARNING/ERROR, Enter to skip): ").strip().upper()
        if lvl == "":
            return None
        if lvl in ("INFO", "WARNING", "ERROR"):
            return lvl
        print("  Level must be INFO, WARNING or ERROR.")

def get_date():
    """Return a YYYY-MM-DD string, or None if skipped. Re-asks on bad dates."""
    while True:
        d = input("Date YYYY-MM-DD (Enter to skip): ").strip()
        if d == "":
            return None
        try:
            dt.datetime.strptime(d, "%Y-%m-%d")
            return d
        except ValueError:
            print("  Invalid date. Example: 2026-11-13")

def get_keyword():
    kw = input("Keyword to search: ").strip()
    return kw or None

def get_path(default="server.log"):
    p = input(f"Log file path [{default}]: ").strip()
    return p or default

def show_entries(entries, limit=10):
    """Print up to `limit` log entries."""
    print(f"\n{len(entries)} matching entries" + (f" (showing first {limit})" if len(entries) > limit else ""))
    for e in entries[:limit]:
        print(f"  {e['timestamp']:%Y-%m-%d %H:%M:%S} | {e['level']:<7} | {e['module']:<8} | {e['message']}")
