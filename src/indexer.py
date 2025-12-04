# src/indexer.py
"""
Indexer: membangun indeks in-memory dari DB untuk pencarian cepat.
- BST: key = title (lowercase), value = list of book ids
- HashTable: key = tag (lowercase), value = set/list of book ids
"""
from data_structures.bst import BST
from data_structures.hashtable import HashTable
from persistence.repo import BookRepo
from typing import List, Set

class Indexer:
    def __init__(self):
        self.title_bst = BST()         # key=title_lower -> value=list of ids
        self.tag_ht = HashTable()      # key=tag_lower -> value=set(ids)

    def build(self):
        self.title_bst = BST()
        self.tag_ht = HashTable()
        books = BookRepo.list_all()
        for b in books:
            key = b.title.lower()
            existing = self.title_bst.find(key)
            if existing is None:
                self.title_bst.insert(key, [b.id])
            else:
                if b.id not in existing:
                    existing.append(b.id)
                    self.title_bst.insert(key, existing)
            # tags
            for tag in b.tags:
                t = tag.strip().lower()
                vals = self.tag_ht.get(t, [])
                if not isinstance(vals, list):
                    vals = list(vals)
                if b.id not in vals:
                    vals.append(b.id)
                self.tag_ht.set(t, vals)

    def search_by_title_exact(self, title: str) -> List[int]:
        res = self.title_bst.find(title.lower())
        return list(res) if res else []

    def search_by_title_prefix(self, prefix: str) -> List[int]:
        # naive: inorder and filter prefix
        res = []
        prefix = prefix.lower()
        for k, v in self.title_bst.inorder():
            if k.startswith(prefix):
                res.extend(v)
        return res

    def search_by_tag(self, tag: str) -> List[int]:
        v = self.tag_ht.get(tag.strip().lower(), [])
        return list(v) if v else []

    def search_by_author(self, author_term: str) -> List[int]:
        # no author index; fallback to scan via BookRepo
        res = []
        term = author_term.lower()
        for b in BookRepo.list_all():
            if term in (b.author or "").lower():
                res.append(b.id)
        return res

    def search_multi(self, title: str = None, author: str = None, tag: str = None) -> List[int]:
        sets = []
        if title:
            # try exact then prefix
            exact = set(self.search_by_title_exact(title))
            pref = set(self.search_by_title_prefix(title))
            s = exact.union(pref)
            sets.append(s)
        if author:
            sets.append(set(self.search_by_author(author)))
        if tag:
            sets.append(set(self.search_by_tag(tag)))
        if not sets:
            return []  # no criteria
        # intersection of all criteria
        res = sets[0]
        for s in sets[1:]:
            res = res.intersection(s)
        return list(res)
