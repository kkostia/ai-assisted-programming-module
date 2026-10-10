# RAG Lab - results

**Date:** 10 October 2026

Measured by running the lab scripts with Python 3.12, all-MiniLM-L6-v2
and a persistent ChromaDB cosine index. Execution was local on Windows;
Codespaces was not accessible from this session.

---

## Part 1: chunking and embeddings (DIY 1 and 2)

- Documents loaded: 5 (1,970 whitespace-separated words in total).
- Chunks produced at 200 words: 14 with 40 words of overlap
  (shortest 72 words, longest 200 words).
- Vector dimensionality: 384.
- Query vector, first five values: `[0.057, 0.040, -0.052, 0.080, -0.100]`.
- Did the query vector have the same dimensionality as the chunks? Yes, 384.

Chunk 1 begins "in half, eliminating the half...", which also appears in
chunk 0. The last 40 words of chunk 0 exactly match the first 40 words of
chunk 1. Both full chunks were printed. All 14 texts, vectors and source
filenames were stored in the `cs_knowledge` collection.

---

## Part 2: retrieval (DIY 3 and 4)

**"what is a variable"** - top hit, score and source: ___

**"how can my code remember a number for later"** - top hit, score and source: ___

_Same meaning, different words: did both queries find the same chunk?_

**"how do I bake sourdough"** - what came back, and with what scores: ___

_One sentence on what a retrieval system does when nothing is relevant:_

---

## Part 3: grounding (DIY 5)

**Q:** What is a variable?
**A:** ___
**Source it cited:** ___

**Q:** How do I bake sourdough?
**A:** ___ (did it decline?)

---

## Part 4: chunk size (DIY 6)

| Chunk size | Right chunk found? | Noise | Notes |
|------------|--------------------|-------|-------|
| 50 words   |                    |       |       |
| 200 words  |                    |       |       |
| 800 words  |                    |       |       |

_One sentence on what goes wrong at each extreme:_

---

## Part 5: long context versus retrieval (DIY 7)

```text
Whole corpus size: ................. [approx tokens]
Question asked: .................... [your question]
  RAG answer: ...................... [response]
  Whole-corpus answer: ............. [response]
Which was better? .................. [RAG / long context / no difference]
At what corpus size would this flip? [your reasoning]
```

Repeat for each of the three questions if the answers differed.

**The question the corpus cannot answer** (sourdough):

- No context: ___
- Whole corpus: ___
- RAG: ___

_Which of the three declined, and what made the difference?_

---

## Reflection

_When would you build retrieval, and when would you just paste everything?_

_What surprised you?_
