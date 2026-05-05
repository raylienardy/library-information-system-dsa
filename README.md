# Sistem Informasi Perpustakaan – Struktur Data (UAS)

## 📚 Library Information System

**Data Structures × SQLite × Tkinter**

A desktop-based Library Information System built with Python, designed to demonstrate practical applications of core data structures in a real-world system.

This project integrates multiple data structures (Stack, Queue, BST, Hash Table, Graph, Heap) with persistent storage (SQLite) and a GUI (Tkinter).

---

## 🚀 Key Features

* **Authentication System**

  * User registration & login
  * Secure password hashing (PBKDF2)

* **Book Management**

  * Full CRUD operations
  * Multi-attribute search (title, author, tags)

* **Borrowing System**

  * Queue-based request handling
  * Transaction tracking

* **Undo System**

  * Stack-based rollback for last transaction

* **Recommendation Engine**

  * Graph-based (co-borrow relationships)
  * Weighted edges + Top-K using Heap

* **Persistence**

  * SQLite database (users, books, transactions)

* **GUI**

  * Built with Tkinter
  * Flow: Login → Dashboard → Book Management → Borrowing

---

## 🧠 Data Structures Mapping

| Feature          | Data Structure           |
| ---------------- | ------------------------ |
| Title search     | Binary Search Tree (BST) |
| Tag indexing     | Hash Table               |
| Borrow queue     | Queue                    |
| Undo transaction | Stack                    |
| Recommendations  | Graph (weighted edges)   |
| Top-K selection  | Heap                     |

---

## 🏗️ System Architecture

```
GUI (Tkinter)
    ↓
Controllers
    ↓
Services Layer
(auth, transaction, recommendation, indexing)
    ↓
Models
(User, Book, Transaction)
    ↓
Persistence Layer (SQLite)
    ↓
Custom Data Structures
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd UAS
```

### 2. Setup Virtual Environment

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
PYTHONPATH=src python - << 'PY'
from persistence.db import init_db
init_db()
PY
```

### 5. Run Application

```bash
PYTHONPATH=src python src/main.py
```

---

## 🧪 Testing

Run all tests:

```bash
PYTHONPATH=src pytest -q
```

---

## 📂 Project Structure

```
src/
├── data_structures/   # Custom implementations
├── persistence/       # SQLite repositories
├── models/            # Domain entities
├── services/          # Business logic
├── controllers/       # GUI interaction layer
├── gui/               # Tkinter UI
├── tests/             # Unit & integration tests
└── main.py            # Entry point
```

---

## 🎯 Design Highlights

* Separation of concerns (MVC-like layering)
* Manual implementation of core data structures
* Real-world simulation (queue, undo, recommendation)
* Testable architecture (services decoupled from GUI)

---

## 📄 Documentation

* `dokumentasi_teknis.pdf` → System design & architecture
* `user_manual.pdf` → End-user guide

---

## ⚠️ Notes

This project was originally developed for academic purposes (Data Structures course), but structured to reflect real-world software engineering practices.

---

## 📜 License

For academic and educational use.
