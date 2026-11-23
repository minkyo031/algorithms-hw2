import unittest
from src.hash_table import HashTable, LinearProbingHashTable, horner
class HashTests(unittest.TestCase):
    def test_both(self):
        for cls in (HashTable, LinearProbingHashTable):
            with self.subTest(cls=cls.__name__):
                t=cls(3)
                self.assertIsNone(t.get('missing'))
                for i in range(25): t.put('key'+str(i),i)
                for i in range(25): self.assertEqual(t.get('key'+str(i)),i)
                t.put('key0',999)
                self.assertEqual(t.get('key0'),999)
                self.assertEqual(t.size,25)
    def test_collision(self):
        for cls in (HashTable,LinearProbingHashTable):
            t=cls(2,max_load=None)
            t.put('a','A');t.put('c','C')
            self.assertEqual(t.get('c'),'C')
    def test_wraparound_and_full(self):
        t=LinearProbingHashTable(3,max_load=None)
        keys=[str(i) for i in range(100) if horner(str(i),3)==2][:3]
        for key in keys: t.put(key,key)
        self.assertEqual(t.slots[2][0],keys[0])
        self.assertEqual(t.slots[0][0],keys[1])
        self.assertEqual(t.slots[1][0],keys[2])
        self.assertEqual(t.get('no-key'),None)
        with self.assertRaises(OverflowError): t.put('another','x')
