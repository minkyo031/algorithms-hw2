"""Additional black-box regression tests for HW2 edge cases."""
import unittest
from src.base62 import encode, decode
from src.hash_table import HashTable, LinearProbingHashTable
from src.shortener import URLShortener


class AdditionalCases(unittest.TestCase):
    def test_base62_boundaries(self):
        for n in (0, 1, 9, 10, 35, 36, 61, 62, 63, 3843, 3844, 10**12):
            with self.subTest(n=n):
                self.assertEqual(decode(encode(n)), n)
        self.assertEqual(encode(0), '0')
        self.assertEqual(encode(61), 'Z')
        self.assertEqual(encode(62), '10')

    def test_replace_in_full_linear_table(self):
        t = LinearProbingHashTable(capacity=2, max_load=None)
        t.put('one', 1)
        t.put('two', 2)
        t.put('one', 3)
        self.assertEqual(t.get('one'), 3)
        self.assertEqual(t.size, 2)
        with self.assertRaises(OverflowError):
            t.put('three', 3)

    def test_collision_and_resizing_preserve_entries(self):
        for cls in (HashTable, LinearProbingHashTable):
            with self.subTest(cls=cls.__name__):
                t = cls(capacity=1, max_load=0.5)
                for i in range(100):
                    t.put(f'https://example.com/{i}', f'code{i}')
                self.assertEqual(t.size, 100)
                for i in range(100):
                    self.assertEqual(t.get(f'https://example.com/{i}'), f'code{i}')
                self.assertIsNone(t.get('not stored'))

    def test_shortener_duplicate_and_missing(self):
        for mode in ('chaining', 'linear'):
            with self.subTest(mode=mode):
                s = URLShortener(mode, capacity=3)
                first = s.shorten('https://example.com/path')
                self.assertEqual(s.shorten('https://example.com/path'), first)
                self.assertEqual(s.resolve(first), 'https://example.com/path')
                self.assertIsNone(s.resolve('not-a-code'))
                second = s.shorten('https://example.com/another')
                self.assertNotEqual(first, second)

    def test_disallowed_schemes_and_spaces(self):
        for mode in ('chaining', 'linear'):
            s = URLShortener(mode)
            for url in ('', 'ftp://example.com', 'https://', 'http://example.com/hello world',
                        ' https://example.com', 'https://example.com:bad', 'https://example.com/'+'x'*2050):
                with self.subTest(mode=mode, url=url[:50]):
                    with self.assertRaises(ValueError):
                        s.shorten(url)


if __name__ == '__main__':
    unittest.main()
