# src/gui/dashboard.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from persistence.repo import BookRepo
from models.book import Book
from session import session_manager
from services.transaction_service import enqueue_request, process_next, undo_last, queue_size
from indexer import Indexer
from services.recommendation import recommend

# Global index instance (rebuilt when needed)
_indexer = Indexer()
_indexer.build()

def refresh_listbox(lb):
    lb.delete(0, tk.END)
    for b in BookRepo.list_all():
        lb.insert(tk.END, f"{b.id} | {b.title} — {b.author} (copies: {b.copies})")

def search_and_show(lb, query):
    # simple search: try title prefix, author and tag
    ids = set()
    if query.strip() == "":
        refresh_listbox(lb)
        return
    # title prefix
    ids.update(_indexer.search_by_title_prefix(query))
    ids.update(_indexer.search_by_title_exact(query))
    ids.update(_indexer.search_by_author(query))
    ids.update(_indexer.search_by_tag(query))
    # show matching books
    lb.delete(0, tk.END)
    for bid in ids:
        b = BookRepo.get_by_id(bid)
        if b:
            lb.insert(tk.END, f"{b.id} | {b.title} — {b.author} (copies: {b.copies})")

def add_book_and_refresh(lb):
    title = simpledialog.askstring("Tambah Buku", "Judul:")
    if not title:
        return
    author = simpledialog.askstring("Tambah Buku", "Author:")
    tags = simpledialog.askstring("Tambah Buku", "Tags (pisah koma):") or ""
    tags_list = [t.strip() for t in tags.split(",") if t.strip()]
    copies = simpledialog.askinteger("Tambah Buku", "Copies:", minvalue=1, initialvalue=1)
    b = Book(id=None, title=title, author=author or "", tags=tags_list, copies=copies or 1)
    bid = BookRepo.add(b)
    _indexer.build()
    refresh_listbox(lb)
    messagebox.showinfo("Tambah Buku", f"Buku ditambahkan id={bid}")

def edit_selected(lb):
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Pilih", "Pilih buku untuk edit")
        return
    entry = lb.get(sel[0])
    book_id = int(entry.split("|",1)[0].strip())
    b = BookRepo.get_by_id(book_id)
    if not b:
        messagebox.showerror("Error", "Buku tidak ditemukan")
        return
    # simple dialogs to edit
    title = simpledialog.askstring("Edit Buku", "Judul:", initialvalue=b.title)
    author = simpledialog.askstring("Edit Buku", "Author:", initialvalue=b.author)
    tags = simpledialog.askstring("Edit Buku", "Tags (pisah koma):", initialvalue=",".join(b.tags))
    copies = simpledialog.askinteger("Edit Buku", "Copies:", minvalue=1, initialvalue=b.copies)
    b.title = title or b.title
    b.author = author or b.author
    b.tags = [t.strip() for t in (tags or "").split(",") if t.strip()]
    b.copies = copies or b.copies
    BookRepo.update(b)
    _indexer.build()
    refresh_listbox(lb)
    messagebox.showinfo("Edit Buku", "Perubahan disimpan")

def delete_selected(lb):
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Pilih", "Pilih buku untuk dihapus")
        return
    entry = lb.get(sel[0])
    book_id = int(entry.split("|",1)[0].strip())
    if not messagebox.askyesno("Hapus", "Yakin hapus buku ini?"):
        return
    ok = BookRepo.delete(book_id)
    if ok:
        _indexer.build()
        refresh_listbox(lb)
        messagebox.showinfo("Hapus", "Buku dihapus")
    else:
        messagebox.showerror("Hapus", "Gagal menghapus")

def borrow_selected(lb):
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Pilih buku", "Pilih buku terlebih dahulu")
        return
    entry = lb.get(sel[0])
    book_id = int(entry.split("|",1)[0].strip())
    if not session_manager.is_authenticated():
        messagebox.showerror("Akses ditolak", "Silakan login terlebih dahulu")
        return
    # enqueue request (user will be processed later)
    enqueue_request(session_manager.get_user_id(), book_id)
    messagebox.showinfo("Antrian", f"Buku id={book_id} ditambahkan ke antrian. Posisi sekarang: {queue_size()}")

def process_queue_now(lb):
    tid = process_next()
    if tid is None:
        messagebox.showinfo("Proses", "Antrian kosong")
    else:
        messagebox.showinfo("Proses", f"Proses selesai, transaction id={tid}")

def undo_last_action(lb):
    ok = undo_last()
    if ok:
        messagebox.showinfo("Undo", "Undo transaksi berhasil")
    else:
        messagebox.showinfo("Undo", "Tidak ada transaksi untuk di-undo")

def show_recommendations_for_selected(lb):
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Pilih", "Pilih buku untuk rekomendasi")
        return
    entry = lb.get(sel[0])
    book_id = int(entry.split("|",1)[0].strip())
    recs = recommend(book_id, k=5)
    if not recs:
        messagebox.showinfo("Rekomendasi", "Tidak ada rekomendasi untuk buku ini")
        return
    txt = "\n".join([f"id={bid} (score={score})" for bid, score in recs])
    messagebox.showinfo("Rekomendasi", txt)

def open_dashboard():
    if not session_manager.is_authenticated():
        messagebox.showerror("Akses", "Tidak ada user yang login")
        return
    username = session_manager.get_username()
    win = tk.Tk()
    win.title(f"Dashboard - {username}")
    win.geometry("820x520")

    top = tk.Frame(win)
    top.pack(fill=tk.X, padx=10, pady=6)

    search_var = tk.StringVar()
    tk.Entry(top, textvariable=search_var, width=60).pack(side=tk.LEFT, padx=6)
    tk.Button(top, text="Cari", command=lambda: search_and_show(lb, search_var.get())).pack(side=tk.LEFT)
    tk.Button(top, text="Segarkan", command=lambda: (_indexer.build(), refresh_listbox(lb))).pack(side=tk.LEFT, padx=6)

    frame = tk.Frame(win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    lb = tk.Listbox(frame, width=110, height=22)
    lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=lb.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb.config(yscrollcommand=scrollbar.set)

    refresh_listbox(lb)

    btn_frame = tk.Frame(win)
    btn_frame.pack(fill=tk.X, padx=10, pady=8)

    tk.Button(btn_frame, text="Tambah Buku", command=lambda: add_book_and_refresh(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Edit", command=lambda: edit_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Hapus", command=lambda: delete_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Pinjam (Antri)", command=lambda: borrow_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Proses Antrian", command=lambda: process_queue_now(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Undo Terakhir", command=lambda: undo_last_action(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Rekomendasi", command=lambda: show_recommendations_for_selected(lb)).pack(side=tk.LEFT, padx=4)
    tk.Button(btn_frame, text="Logout", command=lambda: (session_manager.logout(), win.destroy())).pack(side=tk.RIGHT, padx=4)

    win.mainloop()
