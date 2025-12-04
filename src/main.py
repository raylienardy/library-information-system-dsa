# src/main.py
from persistence.db import init_db
from controllers.app_controller import init_app
from gui.login import main as open_login

def main():
    init_db()
    init_app()
    open_login()

if __name__ == "__main__":
    main()
