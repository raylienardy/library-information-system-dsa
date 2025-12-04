# src/main.py
from persistence.db import init_db
from gui.login import main as open_login

def main():
    init_db()
    open_login()

if __name__ == "__main__":
    main()
