# src/gui/dashboard.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers import app_controller as controller

def refresh_listbox(lb):
    lb.delete(0, tk.END)
    for b in controller.list_books():
        lb.insert(tk.END, f"{b.id} | {b.title} — {b.author} (copies: {b.copies})")

def search_and_show(lb, query):
    if not query.strip():
        refresh_listbox(lb); return
    books = controller.search(title=query, author=query, tag=query)
    lb.delete(0, tk.END)
    for b in books:
        lb.insert(tk.END, f"{b.id} | {b.title} — {b.author} (copies: {b.copies})")

def add_book_and_refresh(lb):
    title = simpledialog.askstring("Tambah Buku", "Judul:")
    if not title: return
    author = simpledialog.askstring("Tambah Buku", "Author:")
    tags = simpledialog.askstring("Tambah Buku", "Tags (pisah koma):") or ""
    tags_list = [t.strip() for t in tags.split(",") if t.strip()]
    copies = simpledialog.askinteger("Tambah Buku", "Copies:", minvalue=1, initialvalue=1)
    bid = controller.add_book(title, author or "", tags_list, copies or 1)
    refresh_listbox(lb)
    messagebox.showinfo("Tambah Buku", f"Buku ditambahkan id={bid}")

def edit_selected(lb):
    sel = lb.curselection()
    if not sel: messagebox.showwarning("Pilih", "Pilih buku untuk edit"); return
    entry = lb.get(sel[0])
    book_id = int(entry.split("|",1)[0].strip())
    b = next((x for x in controller.list_books() if x.id == book_id), None)
    if not b: messagebox.showerror("Error", "Buku tidak ditemukan"); return
    title = simpledialog.askstring("Edit Buku", "Judul:", initialvalue=b.title)
    author = simpledialog.askstring("Edit Buku", "Author:", initialvalue=b.author)
    tags = simpledialog.askstring("Edit Buku", "Tags (pisah koma):", initialvalue=",".join(b.tags))
    copies = simpledialog.askinteger("Edit Buku", "Copies:", minvalue=1, initialvalue=b.copies)
    ok = controller.edit_book(book_id, title or b.title, author or b.author, [t.strip() for t in (tags or "").split(",") if t.strip()], copies or b.copies)
    if ok:
        refresh_listbox(lb)
        messagebox.showinfo("Edit Buku", "Perubahan disimpan")
    else:
        messagebox.showerror("Edit", "Gagal menyimpan perubahan")

def delete_selected(lb):
    sel = lb.curselection()
    if not sel: messagebox.showwarning("Pilih", "Pilih buku"); return
    entry = lb.get(sel[0]); book_id = int(entry.split("|",1)[0].strip())
    if not messagebox.askyesno("Hapus", "Yakin hapus buku ini?"): return
    ok = controller.delete_book(book_id)
    if ok:
        refresh_listbox(lb); messagebox.showinfo("Hapus", "Buku dihapus")
    else:
        messagebox.showerror("Hapus", "Gagal menghapus")

def borrow_selected(lb):
    sel = lb.curselection()
    if not sel: messagebox.showwarning("Pilih buku", "Pilih buku terlebih dahulu"); return
    entry = lb.get(sel[0]); book_id = int(entry.split("|",1)[0].strip())
    try:
        controller.enqueue_borrow(book_id)
    except Exception as e:
        messagebox.showerror("Pinjam", str(e)); return
    messagebox.showinfo("Antrian", f"Buku id={book_id} ditambahkan ke antrian. Posisi: {controller.get_queue_size()}")

def process_queue_now(lb):
    tid = controller.process_next_request()
    if tid is None:
        messagebox.showinfo("Proses", "Antrian kosong")
    else:
        messagebox.showinfo("Proses", f"Proses selesai, transaksi id={tid}")
        refresh_listbox(lb)

def undo_last_action(lb):
    ok = controller.undo_last_transaction()
    if ok:
        messagebox.showinfo("Undo", "Undo transaksi berhasil")
        refresh_listbox(lb)
    else:
        messagebox.showinfo("Undo", "Tidak ada transaksi untuk di-undo")

def show_recommendations_for_selected(lb):
    sel = lb.curselection()
    if not sel: messagebox.showwarning("Pilih", "Pilih buku"); return
    entry = lb.get(sel[0]); book_id = int(entry.split("|",1)[0].strip())
    recs = controller.recommend_for(book_id, k=5)
    if not recs:
        messagebox.showinfo("Rekomendasi", "Tidak ada rekomendasi")
        return
    txt = "\n".join([f"{b.id} | {b.title} (score={score})" for b, score in recs])
    messagebox.showinfo("Rekomendasi", txt)

def open_dashboard():
    username = controller.current_username()
    if not username:
        messagebox.showerror("Akses", "Tidak ada user yang login")
        return
    win = tk.Tk(); win.title(f"Dashboard - {username}"); win.geometry("820x520")
    top = tk.Frame(win); top.pack(fill=tk.X, padx=10, pady=6)
    search_var = tk.StringVar(); tk.Entry(top, textvariable=search_var, width=60).pack(side=tk.LEFT, padx=6)
    tk.Button(top, text="Cari", command=lambda: search_and_show(lb, search_var.get())).pack(side=tk.LEFT)
    tk.Button(top, text="Segarkan", command=lambda: (controller.init_app(), refresh_listbox(lb))).pack(side=tk.LEFT, padx=6)

    frame = tk.Frame(win); frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    lb = tk.Listbox(frame, width=110, height=22); lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lb.yview); scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb.config(yscrollcommand=scrollbar.set)
    refresh_listbox(lb)

    btn_frame = tk.Frame(win); btn_frame.pack(fill=tk.X, padx=10, pady=8)
    tk.Button(btn_frame, text="Tambah Buku", command=lambda: add_book_and_refresh(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Edit", command=lambda: edit_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Hapus", command=lambda: delete_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Pinjam (Antri)", command=lambda: borrow_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Proses Antrian", command=lambda: process_queue_now(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Undo Terakhir", command=lambda: undo_last_action(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Rekomendasi", command=lambda: show_recommendations_for_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Logout", command=lambda: (controller.do_logout(), win.destroy())).pack(side=tk.RIGHT, padx=4)

    win.mainloop()
