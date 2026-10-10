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

**"what is a variable"** - top hit: "Introduction to Programming
Programming is the...", score 0.42, `introduction_to_programming.txt`.
The next hits were the second programming chunk (0.26) and the first
database chunk (0.21); all three passed the 0.20 threshold.

**"how can my code remember a number for later"** - the same top chunk,
score 0.31, `introduction_to_programming.txt`. The next hits were the same
second programming chunk (0.25) and database chunk (0.13); two passed
the 0.20 threshold.

Yes. Both queries returned the same three chunks in the same order even
though their wording differs. Both 500-token context windows used about
321 tokens under the script's character-based estimate.

**"how do I bake sourdough"** - `algorithms_overview.txt` (0.09),
`web_development_intro.txt` (0.09) and `introduction_to_programming.txt`
(0.04). None passed the 0.20 threshold.

Nearest-neighbour search still returns its closest chunks when none is
relevant; low scores and a calibrated threshold are how we recognise
that the corpus contains no useful answer.

---

## Part 3: grounding (DIY 5)

**Q:** What is a variable?
**A:** A variable is like a labeled box that stores information
[source: introduction_to_programming.txt].
**Source it cited:** `introduction_to_programming.txt`.

The retrieved files were `introduction_to_programming.txt` and
`database_fundamentals.txt`. The linked-list question also received an
answer grounded in the retrieved text, citing `data_structures_basics.txt`.

**Q:** How do I bake sourdough?
**A:** I don't know - the provided context does not cover this.

It declined with the exact required sentence and no citation. Its
retrieved files were `algorithms_overview.txt` and `web_development_intro.txt`.
These are actual responses from `gemini-3.5-flash-lite`, using the lab's
configured OpenAI-compatible Gemini endpoint. The prompt explicitly
requires a source for supported answers and no extra text for a refusal.

---

## Part 4: chunk size (DIY 6)

| Chunk size | Right chunk found? | Noise | Notes |
|------------|--------------------|-------|-------|
| 50 words | Yes, for both variable queries | Low in the top hit; some repeated text and control-flow material in the other hits | 66 chunks, 22-50 words. Top scores 0.5778 / 0.4500; 150 words across three hits per query. The definition is split between neighbouring chunks. |
| 200 words | Yes, for both variable queries | Medium: the definition arrives with control structures, functions and an unrelated database chunk | 14 chunks, 32-200 words. Top scores 0.4197 / 0.3088; 512 words across three hits per query. |
| 800 words | Yes, for both variable queries | High: whole programming, database and data-structure documents | 5 chunks, 292-447 words. Top scores 0.4197 / 0.3088; 1,108 words across three hits per query. Each document fits in one chunk. |

All three rebuilds used **20 words of overlap** and were followed by
`python part3_retrieval.py`. Noise is a qualitative assessment of the
returned text; the word totals above measure the unfiltered three hits,
including overlap, before the separate 500-token context budget.

At 50 words, chunks can begin or end mid-sentence and separate a
definition from its supporting example; at 800 words, each hit includes a
whole document with many topics unrelated to the question.

For sourdough, the three scores were:

- 50 words: 0.1286, 0.1175, 0.0928 (two programming chunks and an
  algorithms chunk).
- 200 words: 0.0878, 0.0863, 0.0524 (algorithms, web development,
  algorithms).
- 800 words: 0.0878, 0.0863, 0.0367 (algorithms, web development,
  programming).

None passed 0.20 at any size. At 200 words with overlap 20, the second
hit for the paraphrased variable question scored 0.1992: it prints as
0.20 but does not pass the threshold. The index was restored with
`python part2_embeddings.py --chunk-words 200` (default overlap 40)
before the generation and long-context comparison.

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
