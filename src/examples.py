from data_structures.bst import BST
from data_structures.graph import Graph
from data_structures.hashtable import HashTable
from data_structures.queue import Queue
from data_structures.stack import Stack

bst = BST()
bst.insert("C", 3)
bst.insert("A", 1)
bst.insert("B", 2)
print("BST inorder:", bst.inorder())

s = Stack()
s.push("undo1")
s.push("undo2")
print("Stack pop:", s.pop())

q = Queue()
q.enqueue("req1")
q.enqueue("req2")
print("Queue dequeue:", q.dequeue())

ht = HashTable()
ht.set("id1", {"title": "Buku A"})
print("Get id1:", ht.get("id1"))

g = Graph()
g.add_edge(1, 2, weight=3)
g.add_edge(1, 3, weight=1)
print("Neighbors of 1:", g.neighbors(1))
