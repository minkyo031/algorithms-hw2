"""Base62 encoding using digits, lower-case then upper-case letters."""
ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encode(n):
    if type(n) is not int or n < 0:
        raise ValueError('expected nonnegative integer')
    if n == 0: return '0'
    out = ''
    while n:
        n, digit = divmod(n, 62)
        out = ALPHABET[digit] + out
    return out

def decode(s):
    if not isinstance(s, str) or not s:
        raise ValueError('invalid code')
    n = 0
    for ch in s:
        digit = ALPHABET.find(ch)
        if digit < 0: raise ValueError('invalid code character')
        n = n * 62 + digit
    return n
