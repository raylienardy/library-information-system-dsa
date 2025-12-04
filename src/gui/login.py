# src/gui/login.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from services.user_service import register_user, login_user, UserExistsError, AuthError
from session import session_manager
from gui.dashboard import open_dashboard


def on_login(root, username_var, password_var):
    username = username_var.get().strip()
    password = password_var.get()
    try:
        user = login_user(username, password)
    except AuthError as e:
        messagebox.showerror("Login gagal", str(e))
        return
    # sukses: simpan session dan buka dashboard
    session_manager.login(user.id, user.username)
    messagebox.showinfo("Login", f"Selamat datang, {user.username}")
    root.destroy()
    open_dashboard()

def on_register():
    # dialog register sederhana
    dlg = tk.Tk()
    dlg.withdraw()  # sembunyikan window utama dialog
    username = simpledialog.askstring("Register", "Username:", parent=dlg)
    if not username:
        return
    password = simpledialog.askstring("Register", "Password:", parent=dlg, show="*")
    if not password:
        return
    try:
        user = register_user(username.strip(), password)
    except UserExistsError:
        messagebox.showwarning("Register", "Username sudah ada, coba username lain")
        return
    except Exception as e:
        messagebox.showerror("Register", f"Gagal register: {e}")
        return
    messagebox.showinfo("Register", f"User '{user.username}' berhasil dibuat (id={user.id})")

def main():
    root = tk.Tk()
    root.title("Login - Perpustakaan")
    root.geometry("360x240")
    tk.Label(root, text="Login Perpustakaan", font=("Arial", 14)).pack(pady=8)

    frm = tk.Frame(root)
    frm.pack(pady=4)
    tk.Label(frm, text="Username").grid(row=0, column=0, sticky="w", padx=6, pady=4)
    username_var = tk.StringVar()
    tk.Entry(frm, textvariable=username_var).grid(row=0, column=1)

    tk.Label(frm, text="Password").grid(row=1, column=0, sticky="w", padx=6, pady=4)
    password_var = tk.StringVar()
    tk.Entry(frm, textvariable=password_var, show="*").grid(row=1, column=1)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=12)
    tk.Button(btn_frame, text="Login", width=10, command=lambda: on_login(root, username_var, password_var)).pack(side=tk.LEFT, padx=8)
    tk.Button(btn_frame, text="Register", width=10, command=on_register).pack(side=tk.LEFT, padx=8)
    tk.Button(btn_frame, text="Keluar", width=10, command=root.destroy).pack(side=tk.LEFT, padx=8)

    root.mainloop()

if __name__ == "__main__":
    main()
