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

At 800 words, the printed overlap check is False because chunks 0 and 1
come from different documents; there are no neighbouring chunks within
any one document at this size, so overlap does not apply.

---

## Part 5: long context versus retrieval (DIY 7)

```text
Whole corpus size: 2626 approximate tokens (1970 words / 0.75).
Question asked: What is a variable?
  RAG answer: A variable is like a labeled box that stores information [source: introduction_to_programming.txt].
  Whole-corpus answer: A variable is like a labeled box that stores information [source: introduction_to_programming.txt].
Which was better? No difference; the answers are identical.
At what corpus size would this flip? When the whole corpus exceeds the context budget or sending it for every question becomes too expensive. For example, a 10,000-token budget for documents allows roughly 7,500 words; larger corpora would need selection or retrieval under that budget. This is a conditional budget, not the Gemini model's context limit.
```

**Question asked:** How do linked lists work?

**RAG answer:** Linked lists are a linear data structure where elements
are not stored contiguously. Instead, each element (called a node)
contains data and a reference (or link) to the next node. There are two
main types: singly linked lists where each node points to the next, and
doubly linked lists where nodes point both forward and backward
[source: data_structures_basics.txt].

**Whole-corpus answer:** A linked list is a linear data structure where
elements are not stored contiguously. Instead, each element (called a
node) contains data and a reference (or link) to the next node. There are
two main types: singly linked lists where each node points to the next,
and doubly linked lists where nodes point both forward and backward.
Linked lists excel at insertions and deletions because you only need to
update pointers, not shift all elements like in an array
[source: data_structures_basics.txt].

**Which was better?** Long context was slightly more complete in this run:
it also explained the insertion/deletion advantage. Both answers were
correctly grounded and cited the same file; one run does not establish a
general quality advantage.

**Question asked:** What is HTML?

**RAG answer:** HTML (HyperText Markup Language) provides the structure and
content of web pages, using tags to define elements like headings,
paragraphs, links, and images [source: web_development_intro.txt].

**Whole-corpus answer:** HTML (HyperText Markup Language) provides the
structure and content of web pages [source: web_development_intro.txt].

**Which was better?** Both answered correctly; RAG included more detail
about tags in this run. The simpler whole-corpus approach still answered
the question without needing an embedding model or vector database.

The comparison used the same questions, model and `GROUNDING_RULES` in
both methods. RAG used the restored 200-word/40-overlap index and top-k 3;
the whole-corpus prompt concatenated all five source-labelled documents.
The 2,626-token estimate counts document text only, excluding source
labels, instructions and the question. RAG's response cap was 500 tokens
and the whole-corpus cap was 300, as supplied in the lab.

The supplied top-k experiment also measured 266, 709 and 1,072 approximate
context tokens for k=1, 3 and 5. At k=1 the source was programming; k=3
added databases; k=5 also added data structures. More retrieved text was
not automatically more relevant to the variable question.

**The question the corpus cannot answer** (sourdough):

- No context: the model supplied a five-step sourdough recipe: feed a
  starter, mix dough, ferment, shape and refrigerate, then bake. It did
  not decline and relied on knowledge outside this corpus.
- Whole corpus: "I don't know - the provided context does not cover this."
- RAG: "I don't know - the provided context does not cover this."

Both grounded approaches declined with the exact required sentence and
no citation. The explicit instruction to use only the provided context
and to permit "I don't know" made the difference; retrieval alone did
not, because it still returned unrelated chunks.

---

## Reflection

For this five-document, 1,970-word corpus, the whole text fits comfortably
in a single prompt and gave correct, cited answers, so retrieval adds
infrastructure without a demonstrated need. Retrieval becomes useful
when the corpus grows beyond the available context budget, sending all
documents repeatedly costs too much, or questions need targeted access
to frequently updated sources. Its usefulness depends on measured
retrieval quality as well as size.

The paraphrased variable question found the same top chunk as the direct
question, but an entirely unrelated sourdough question still returned
three chunks. Another useful result was that a score displayed as 0.20
could fail a 0.20 threshold because the unrounded score was 0.1992.
