# SPEC: URL Shortener

## 1. Goal
Create an HTTP(S) URL shortening service powered by a custom Horner-hashed table. Support both separate chaining and linear probing without Python dict/set/hash in `src/`.

## 2. Encoding
`encode(n)` uses 0-9, a-z, A-Z in that order, with zero encoded as `0`; `decode(s)` is inverse. Reject negatives, empty codes and unsupported characters.

## 3. Data structures
`HashTable(capacity,max_load)` is separate chaining implemented with linked nodes. `LinearProbingHashTable` uses open addressing, wraps around the last slot, and raises `OverflowError` if full and resizing is disabled. Both support `put`, `get`, `get_with_cost`, `entries`. Repeated keys replace values without increasing size. Horner hash computes `(31*h+ord(c)) % capacity` for each character. Automatic resize when max_load is enabled, disabled with `max_load=None`.

## 4. Shortener
`URLShortener(table_type='chaining'|'linear')` stores URL-to-code and code-to-URL mappings using custom tables. Unique sequential integers beginning at 1 are encoded with Base62; they are **not** derived from hashes. Repeated identical URLs return the original code. Unknown code returns `None`. Data is in-memory, so restarting clears it.

## 5. Web UI
`/` presents input and an algorithm selector; POST `/shorten` returns a clickable link; `/<mode>/<code>` redirects to the URL; `/table` shows table slots, keys, values, links, Horner computations and linear-probe displacement. On Codespaces, forwarded host/protocol headers are preferred to local headers.

## 6. Edge cases and validation
Only absolute `http://` and `https://` URLs. Reject blank strings, whitespace and control characters, `ftp://` or missing host, invalid ports, and URLs longer than 2048 characters. Test Base62 0/61/62; collision, wraparound, full linear table; duplicate inserts; missing keys; growing tables; identical URLs; distinct URLs; and invalid URL inputs.

## 7. Experiments
Fixed M=4093 and `max_load=None`. Chaining alpha=0.25..4. Compare both tables alpha=0.1..0.9 with matching input keys and capacity. Record mean successful/failed lookup cost and compare to theoretical formulas. Chaining counts nodes compared; linear probing counts slots inspected (including the terminating empty slot).

8. Error Handling

Invalid URL input must not create a shortened URL.

The web interface must display an error message when URL validation fails.

Requests for unknown short codes must return HTTP 404.

The service must continue running after invalid input without losing existing mappings.
