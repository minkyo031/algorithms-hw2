import unittest
from src.base62 import encode, decode
class Base62Tests(unittest.TestCase):
    def test_edges(self):
        for n, s in [(0,'0'),(9,'9'),(10,'a'),(35,'z'),(36,'A'),(61,'Z'),(62,'10'),(3843,'ZZ'),(3844,'100')]:
            self.assertEqual(encode(n),s)
            self.assertEqual(decode(s),n)
    def test_roundtrip(self):
        for n in (1, 100, 100000000, 2**64): self.assertEqual(decode(encode(n)),n)
    def test_invalid(self):
        for bad in (-1, 1.5, '2'):
            with self.assertRaises(ValueError): encode(bad)
        for bad in ('','abc!',None):
            with self.assertRaises(ValueError): decode(bad)
