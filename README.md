# Sistem Informasi Perpustakaan – Struktur Data (UAS)

Proyek ini adalah aplikasi Sistem Informasi Perpustakaan berbasis Python yang
menggabungkan _Data Structures_, _SQLite persistence_, dan _GUI Tkinter_ sebagai
implementasi UAS Mata Kuliah Struktur Data.

## ✨ Fitur Utama

- Registrasi & Login (password hashing PBKDF2)
- Manajemen Buku (CRUD)
- Pencarian multi-kriteria (title, author, tag)
- Antrian peminjaman (Queue)
- Riwayat & Undo transaksi (Stack)
- Rekomendasi buku berbasis Graph (co-borrow)
- Penyimpanan data SQLite (users, books, transactions)
- GUI Tkinter: Login → Dashboard → Kelola Buku → Peminjaman

---

## 📦 Instalasi

### 1. Clone repository

```bash
git clone <repository-anda>
cd UAS
```

````

### 2. Buat virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Inisialisasi database

```bash
PYTHONPATH=src python - << 'PY'
from persistence.db import init_db
init_db()
PY
```

### 5. Jalankan aplikasi

```bash
PYTHONPATH=src python src/main.py
```

---

## 🧪 Testing

Jalankan semua unit test:

```bash
PYTHONPATH=src pytest -q
```

---

## 🧱 Struktur Folder

```
src/
 ├── data_structures/   # Stack, Queue, BST, HashTable, Graph, Heap
 ├── persistence/       # SQLite + Repository
 ├── models/            # Book, User, Transaction
 ├── services/          # Auth, Transaction, Recommendation, Indexer
 ├── gui/               # Tkinter UI
 ├── controllers/       # Penghubung GUI ↔ services
 ├── tests/             # Unit & integration tests
 └── main.py            # Entry point aplikasi
```

---

## 👨‍💻 Teknologi yang Digunakan

- Python 3.x
- Tkinter GUI
- SQLite3
- Data Structures Implementations (manual)
- pytest (unit test)
- flake8 (linting)

---

## 📝 Lisensi

Proyek UAS – digunakan untuk keperluan akademik.

```

---

# 2️⃣ Buat `dokumentasi_teknis.pdf`
Aku siapkan **isi lengkapnya**, kamu tinggal copy ke Word/Docs → Save as PDF.

🔽 **ISI LENGKAP DOKUMEN (paste ke Word/Google Docs):**

---

# **DOKUMENTASI TEKNIS**
## Sistem Informasi Perpustakaan – Struktur Data

### 1. Pendahuluan
Proyek ini dibangun sebagai implementasi UAS Mata Kuliah Struktur Data.
Tujuan proyek adalah mengintegrasikan berbagai struktur data (Stack, Queue, BST,
HashTable, Graph, Heap) ke dalam sebuah aplikasi perpustakaan nyata dengan
GUI serta penyimpanan data SQLite.

---

## 2. Arsitektur Sistem

### **Diagram Arsitektur**
```

GUI Tkinter
│
▼
Controllers
│
Services Layer
(auth, transaction, recommendation, indexer)
│
Models (User, Book, Transaction)
│
Persistence (SQLite Repo)
│
Data Structures
(Stack, Queue, BST, HashTable, Graph, Heap)

```

---

## 3. Entity Relationship Diagram (ERD)

```

Users (id, username, password_hash, role)
Books (id, title, author, tags, copies)
Transactions (id, user_id, book_id, action, timestamp)

````

Relasi:

- One User → Many Transactions
- One Book → Many Transactions

---

## 4. Struktur Data yang Digunakan

| Fitur                | Struktur Data                 |
| -------------------- | ----------------------------- |
| Search katalog title | BST                           |
| Index tag → buku     | HashTable                     |
| Antrian peminjaman   | Queue                         |
| Undo transaksi       | Stack                         |
| Rekomendasi buku     | Graph (co-borrow edge weight) |
| top-k rekomendasi    | Heap                          |

Penjelasan implementasi terlampir di kode `src/data_structures`.

---

### 5. Algoritma Penting

#### 5.1 Pencarian Buku

- BST digunakan untuk index judul → search O(log n)
- HashTable untuk lookup tag → O(1)

#### 5.2 Peminjaman Buku

- enqueue_request() → Queue
- process_next() → memproses antrian & mencatat transaksi
- undo_last() → Stack pop untuk rollback

#### 5.3 Rekomendasi

- Graph adjacency list: book_a ↔ book_b
- Bobot = jumlah co-borrow
- recommend(book_id, k) → ambil tetangga berbobot tertinggi

---

## 6. Unit Test & Integrasi

- Semua unit test (`pytest`) lulus tanpa error
- Integration test: register → add book → borrow → undo → rekomendasi

---

## 7. Kesimpulan

Aplikasi memenuhi seluruh requirement UAS:

- Memakai ≥ 6 struktur data
- Ada GUI
- Ada pencarian, CRUD, transaksi, undo, rekomendasi
- Ada database persistence
- Semua diuji (unit + integrasi)

---

# **User Manual – Sistem Informasi Perpustakaan**

## 1. Pembukaan

Manual ini membantu pengguna mengoperasikan aplikasi perpustakaan.

---

## 2. Cara Menjalankan Aplikasi

1. Aktifkan virtual environment
2. Jalankan:

```bash
PYTHONPATH=src python src/main.py
```

3. Akan muncul tampilan Login.

---

## 3. Registrasi Akun

1. Klik _Register Account_
2. Masukkan:
   - Username
   - Password

3. Akun akan tersimpan di database.

---

## 4. Login

1. Masukkan username & password
2. Jika benar → masuk ke Dashboard

---

## 5. Dashboard

Menu utama:

- List Buku
- Cari Buku
- Tambah Buku
- Pinjam Buku
- Undo Peminjaman
- Rekomendasi
- Logout

---

## 6. Cara Menambah Buku

1. Klik "Tambah Buku"
2. Isi judul, penulis, tags, jumlah kopi
3. Klik "Add"

---

## 7. Cara Meminjam Buku

1. Pilih buku di daftar
2. Klik tombol **Pinjam**
3. Transaksi akan tercatat

---

## 8. Undo Peminjaman

Klik tombol _Undo Last Transaction_ → transaksi terakhir dihapus.

---

## 9. Rekomendasi Buku

1. Pilih satu buku
2. Klik "Rekomendasi"
3. Aplikasi menampilkan buku-buku yang paling sering dipinjam bersama (co-borrow graph)

---

## 10. Troubleshooting

- Tidak bisa login → cek password
- Buku tidak muncul → refresh atau restart aplikasi
- Antrian kosong → belum ada permintaan peminjaman
