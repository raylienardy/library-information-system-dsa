# src/services/recommendation.py
from data_structures.graph import Graph
from persistence.repo import TransactionRepo, BookRepo
from collections import defaultdict
from typing import List, Tuple

def build_coborrow_graph() -> Graph:
    """
    Build undirected weighted graph: nodes = book_id
    For each user, consider the set of book_ids they borrowed and increase weight for each pair.
    """
    g = Graph()
    # gather books per user
    # naive: read all transactions and group by user
    txs_by_user = defaultdict(list)
    for btx in TransactionRepo.list_all():  # but TransactionRepo.list_all not implemented — we can instead query DB directly
        pass
    # fallback: implement below using DB directly
    from persistence.db import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id, book_id FROM transactions")
    rows = cur.fetchall()
    conn.close()
    for r in rows:
        txs_by_user[r["user_id"]].append(r["book_id"])
    # for each user, count pairwise co-borrows
    for user, borrows in txs_by_user.items():
        unique_books = list(set(borrows))
        n = len(unique_books)
        for i in range(n):
            for j in range(i+1, n):
                a = unique_books[i]; b = unique_books[j]
                g.add_edge(a, b, weight=1.0)
    return g

def recommend(book_id: int, k: int = 3) -> List[Tuple[int, float]]:
    """
    Return top-k recommended book ids as list of (book_id, score) sorted desc by score.
    """
    g = build_coborrow_graph()
    neigh = g.neighbors(book_id)  # dict neighbor->weight
    if not neigh:
        return []
    # sort by weight desc
    sorted_items = sorted(neigh.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:k]
