# Algorithms HW2 — URL Shortener

Python standard library implementation of two hash tables and a URL shortening website.

## Quickstart

```bash
make test
make experiment
make serve
```

Then visit http://localhost:8000 . Choose chaining or linear probing; submit an absolute HTTP(S) URL, follow its shortened link, or inspect the internal storage at `/table`.

The two table variants are `HashTable` (separate chaining) and `LinearProbingHashTable` (linear probing). Both are based on Horner hashing and support `get_with_cost`. The project does not use `dict`, `set`, or built-in `hash()` in `src/`.

## Experiments

`make experiment` produces:
- `experiments/results.csv`, `experiments/chaining.svg` (chaining at alpha 0.25–4)
- `experiments/comparison.csv`, `experiments/comparison_success.svg`, `experiments/comparison_failure.svg` (two implementations at alpha 0.1–0.9)

The experiments use deterministic seed-generated URL keys, fixed M=4093, and 1,000 successful and 1,000 unsuccessful lookups per configuration. Measurements are reproducible. No external libraries.

## Important limits

- In-memory data is reset on restart.
- Starting template was not directly cloned; this is a standalone implementation with matching named directories/commands. Transfer files into a repository created from the official template after reviewing it.
- GitHub Issues, Copilot agent history, authentic human edits, feature branches, GitHub pushes, actual mobile testing, and personalized report details cannot be fabricated. Complete them in your own GitHub account and verify the final public URL.
