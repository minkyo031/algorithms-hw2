"""URL shortener using two custom hash tables for both directions."""
from urllib.parse import urlsplit
from .base62 import encode
from .hash_table import HashTable, LinearProbingHashTable

class URLShortener:
    def __init__(self, table_type='chaining', capacity=97, max_load=0.75):
        if table_type not in ('chaining', 'linear'):
            raise ValueError('table_type must be chaining or linear')
        cls = HashTable if table_type == 'chaining' else LinearProbingHashTable
        self.url_to_code = cls(capacity, max_load)
        self.code_to_url = cls(capacity, max_load)
        self.table_type = table_type
        self.next_id = 1

    @staticmethod
    def validate(url):
        if not isinstance(url, str) or not url or url != url.strip() or len(url) > 2048:
            raise ValueError('URL must have 1-2048 characters and no surrounding spaces')
        if any(ch.isspace() or ord(ch) < 32 for ch in url):
            raise ValueError('URL cannot contain whitespace or control characters')
        parts = urlsplit(url)
        if parts.scheme not in ('http', 'https') or not parts.netloc or not parts.hostname:
            raise ValueError('Only absolute HTTP(S) URLs are supported')
        try: _ = parts.port
        except ValueError as exc: raise ValueError('Invalid port') from exc
        return url

    def shorten(self, url):
        url = self.validate(url)
        existing = self.url_to_code.get(url)
        if existing is not None: return existing
        code = encode(self.next_id)
        self.url_to_code.put(url, code)
        self.code_to_url.put(code, url)
        self.next_id += 1
        return code

    def resolve(self, code):
        return self.code_to_url.get(code)
