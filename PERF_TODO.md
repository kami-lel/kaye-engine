# Performance TODO

<!-- Todo: memoize `BasePromptNode` lineage / hash to kill O(N) recompute -->

Recorded performance ideas to pick up later. Each entry states the problem,
the evidence, a concrete implementation sketch, and how to verify the win.

----


### Problem

`kaye/prompt/base_prompt_node.py::generate_lineage()` walks from a node up to
the root and rebuilds a fresh `list` of names on **every call**. It is called
from both `__hash__` and `__eq__`:

```python
def __hash__(self):
    return hash(tuple(self.generate_lineage()))

def __eq__(self, other):
    # compares self.generate_lineage() against other.generate_lineage()
    ...
```

Because `is_checkmarked()` and `generate_prompt_lines()` hash/compare nodes in
tight loops, this immutable data is recomputed millions of times per render.

### Evidence (cProfile of `python -m kaye claude skill <folder>`)

- one full export of the 84 skills takes ~10 s wall (interpreter + import is
  only ~0.39 s, so the cost is the render, not startup)
- `generate_lineage()` is called **~33 million times** (~16 s `tottime`)
- `__hash__` ~9.2M calls, `__eq__` ~4.5M calls — all funnelling into
  `generate_lineage()`
- the test suite pays this ~9× over (one full export per session-scoped
  fixture across `tests/cli/a/*` and `tests/cli/c/*`), which is ~70–80 s of
  the ~82 s total run time

### Why memoization is safe

A node's `parent` and `name` are fixed once the corpus is parsed; blueprint
checkmarking changes a *separate* checkmark set, not the tree's name/parent
structure. So a node's lineage (and therefore its hash) is immutable for the
node's lifetime. It only needs invalidation if the tree is mutated after
construction (re-parenting / rename), which the render path does not do.

### Implementation sketch

Option A — cache the lineage list lazily:

```python
def generate_lineage(self):
    cached = self.__dict__.get("_lineage_cache")
    if cached is not None:
        return list(cached)          # return a copy; callers append to it

    if self.is_root:
        lineage = []
    else:
        lineage = self.parent.generate_lineage()
        lineage.append(self.name)

    self.__dict__["_lineage_cache"] = tuple(lineage)
    return lineage
```

Option B — memoize the hash directly (cheapest for the hot path):

```python
def __hash__(self):
    cached = self.__dict__.get("_hash_cache")
    if cached is None:
        cached = hash(tuple(self.generate_lineage()))
        self.__dict__["_hash_cache"] = cached
    return cached
```

Notes / cautions:

- `anytree` may use `__slots__` in some versions — if so, add the cache
  attribute name to the node's slots, or store in a side dict keyed by `id`.
- if any code re-parents or renames a node after construction, clear
  `_lineage_cache` / `_hash_cache` there (search for `.parent =` and `.name =`
  assignments on nodes).
- keep `generate_lineage()` returning a fresh list (callers like the original
  `append(self.name)`); only the *cache* is the shared tuple.

### Verification

```bash
# before/after, one export
rm -rf /tmp/x && time python -m kaye claude skill /tmp/x

# full suite timing
time pytest

# correctness: output must be byte-identical before vs after
python -m kaye claude skill /tmp/before
# (apply change)
python -m kaye claude skill /tmp/after
diff -r /tmp/before /tmp/after   # expect no differences
```

Target: per-export ~10 s → ~1–2 s; full suite ~82 s → ~25–30 s; CLI snappier
for real users too.
