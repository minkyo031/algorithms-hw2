"""Separate chaining and linear probing maps; no built-in hash containers."""

def horner(key, capacity):
    if not isinstance(key, str): raise TypeError('keys must be strings')
    h = 0
    for ch in key:
        h = (31 * h + ord(ch)) % capacity
    return h

def horner_steps(key, capacity):
    h = 0
    steps = []
    for ch in key:
        old = h
        h = (31 * h + ord(ch)) % capacity
        steps.append((repr(ch), old, ord(ch), h))
    return steps

class Node:
    def __init__(self, key, value, next_node=None):
        self.key, self.value, self.next = key, value, next_node

class HashTable:
    def __init__(self, capacity=97, max_load=0.75):
        if capacity < 1: raise ValueError('capacity must be positive')
        self.capacity, self.max_load, self.size = capacity, max_load, 0
        self.buckets = [None] * capacity

    def _resize(self):
        old = self.buckets
        self.capacity = self.capacity * 2 + 1
        self.buckets = [None] * self.capacity
        self.size = 0
        for head in old:
            while head is not None:
                self.put(head.key, head.value)
                head = head.next

    def put(self, key, value):
        idx = horner(key, self.capacity)
        cur = self.buckets[idx]
        while cur:
            if cur.key == key:
                cur.value = value
                return
            cur = cur.next
        if self.max_load is not None and (self.size + 1) / self.capacity > self.max_load:
            self._resize()
            idx = horner(key, self.capacity)
        self.buckets[idx] = Node(key, value, self.buckets[idx])
        self.size += 1

    def get_with_cost(self, key):
        idx = horner(key, self.capacity)
        cur, comparisons = self.buckets[idx], 0
        while cur:
            comparisons += 1
            if cur.key == key: return cur.value, comparisons
            cur = cur.next
        return None, comparisons

    def get(self, key): return self.get_with_cost(key)[0]

    def entries(self):
        for i, head in enumerate(self.buckets):
            cur = head
            while cur:
                yield (i, cur.key, cur.value)
                cur = cur.next

class LinearProbingHashTable:
    def __init__(self, capacity=97, max_load=0.75):
        if capacity < 1: raise ValueError('capacity must be positive')
        self.capacity, self.max_load, self.size = capacity, max_load, 0
        self.slots = [None] * capacity

    def _resize(self):
        old = self.slots
        self.capacity = self.capacity * 2 + 1
        self.slots = [None] * self.capacity
        self.size = 0
        for item in old:
            if item is not None: self.put(item[0], item[1])

    def put(self, key, value):
        start = horner(key, self.capacity)
        for offset in range(self.capacity):
            idx = (start + offset) % self.capacity
            item = self.slots[idx]
            if item is not None and item[0] == key:
                self.slots[idx] = (key, value)
                return
            if item is None: break
        else:
            if self.max_load is None: raise OverflowError('hash table full')
            self._resize()
            return self.put(key, value)
        if self.max_load is not None and (self.size + 1) / self.capacity > self.max_load:
            self._resize()
            return self.put(key, value)
        self.slots[idx] = (key, value)
        self.size += 1

    def get_with_cost(self, key):
        start = horner(key, self.capacity)
        for offset in range(self.capacity):
            idx = (start + offset) % self.capacity
            item = self.slots[idx]
            if item is None: return None, offset + 1
            if item[0] == key: return item[1], offset + 1
        return None, self.capacity

    def get(self, key): return self.get_with_cost(key)[0]

    def entries(self):
        for i, item in enumerate(self.slots):
            if item is not None: yield (i, item[0], item[1])
