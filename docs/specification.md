# Specification & Requirements

**Project:** [NIM] - Sistem Perpustakaan Digital (Project Mata Kuliah Struktur Data)  
**Sumber requirement:** FORMAT TUGAS PROYEK MATA KULIAH STRUKTUR DATA. :contentReference[oaicite:2]{index=2}

## 1. Ringkasan requirement (ekstrak dari dokumen)

- Proyek harus menggunakan **≥ 6 jenis struktur data** (mis. BST, Hash Table, Stack, Queue, Graph, Heap/Array).
- Fitur minimal: manajemen buku, pencarian multi-kriteria, sistem peminjaman (antrian), manajemen user (autentikasi), rekomendasi sederhana, analytics/top-k.
- Persistensi data wajib (SQLite atau file JSON).
- Deliverables: source code, database contoh, dokumentasi teknis (PDF), user manual (PDF), laporan proyek (format tugas).
- Unit tests & integration tests direkomendasikan.

## 2. Daftar fitur wajib (prioritas)

1. Autentikasi user (register/login) + manajemen user.
2. CRUD buku (tambah/ubah/hapus/list).
3. Pencarian multi-kriteria (title, author, tag).
4. Sistem peminjaman (queue untuk antrian permintaan).
5. Undo/History (stack) untuk operasi kritis.
6. Rekomendasi berbasis graph (co-borrow).
7. Analytics: top-k buku dipinjam, frekuensi penulis, dsb.
8. Persistensi (SQLite) + backup sample DB.

## 3. Non-functional requirements

- Bahasa: Python 3.11+
- UI: Tkinter (desktop) atau CLI; opsi web (Flask) jika diperlukan.
- Testing: pytest atau unittest.
- Code style: modular, OOP, docstring.
- Dokumentasi: ERD, arsitektur, run instructions, test instructions.

## 4. Deliverables (format & lokasi)

- `src/` — source code terstruktur.
- `data/library.db` atau `data/sample_data.json` — contoh DB.
- `docs/dokumentasi_teknis.pdf` — ERD + penjelasan modul.
- `docs/user_manual.pdf` — langkah penggunaan & screenshot.
- `docs/laporan_proyek.pdf` — laporan sesuai template tugas.
- `tests/` — unit & integration tests.

## 5. Mapping fitur → struktur data (preview)

(Lihat bagian mapping di bawah untuk detail implementasi.)

## 6. Acceptance Criteria (kriteria penerimaan)

- Semua fitur wajib bisa dijalankan pada mesin developer dengan instruksi di README.
- Unit tests utama lulus (`python -m pytest -q`).
- Dokumentasi terisi sesuai template tugas.

## Mapping fitur ↔ Struktur Data (Detail)

| Fitur aplikasi                    | Struktur Data utama               | Alasan / penggunaan                                       |
| --------------------------------- | --------------------------------- | --------------------------------------------------------- |
| Indeks katalog berdasarkan judul  | BST (key = title)                 | Traversal inorder → sorted listing; search by range/title |
| Lookup cepat (id, tags)           | Hash Table (separate chaining)    | Akses O(1) average untuk id / tag → list book ids         |
| Antrian peminjaman                | Queue                             | FIFO processing request pinjam                            |
| Undo / riwayat operasi            | Stack                             | Undo terakhir (LIFO)                                      |
| Rekomendasi co-borrow             | Graph (adjacency list, weighted)  | Node = buku, edge weight = banyak co-borrow               |
| Top-k analytics (buku terpopuler) | Heap / Partial sort (array utils) | Ambil top-k frekuensi pinjaman                            |
| Penyimpanan sementara / cache     | Dictionary / HashTable            | Cache lookup, session storage                             |
