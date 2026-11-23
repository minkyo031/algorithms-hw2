import unittest
from src.shortener import URLShortener
class ShortenerTests(unittest.TestCase):
    def test_both(self):
        for mode in ('chaining','linear'):
            with self.subTest(mode=mode):
                s=URLShortener(mode,capacity=3)
                a='https://example.com/one'
                self.assertEqual(s.shorten(a),'1')
                self.assertEqual(s.shorten(a),'1')
                self.assertEqual(s.shorten('https://example.com/two'),'2')
                self.assertEqual(s.resolve('1'),a)
                self.assertIsNone(s.resolve('missing'))
                for i in range(70):
                    url='https://example.org/'+str(i)
                    self.assertEqual(s.resolve(s.shorten(url)),url)
                self.assertEqual(s.shorten('https://example.com/third'),'1b')
    def test_bad_urls(self):
        s=URLShortener()
        for url in ('','ftp://example.com','example.com',' https://example.com','https://example.com\n','https://example.com/a b','https://','https://example.com:'+'x', 'https://example.com/'+'x'*2050):
            with self.subTest(url=url[:50]), self.assertRaises(ValueError): s.shorten(url)
