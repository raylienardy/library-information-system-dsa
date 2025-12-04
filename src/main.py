# src/main.py
from controllers.app_controller import init_app
from gui.login import main as open_login
from persistence.db import init_db


def main():
    init_db()
    init_app()
    open_login()


if __name__ == "__main__":
    main()
