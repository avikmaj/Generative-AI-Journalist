---
name: rag-pipeline-designer
description: "Design and debug retrieval-augmented generation end to end: parsing, chunking and overlap, embeddings and vector stores, retrieval symmetry, answer synthesis, and retrieval-quality evaluation. Load when the user asks about RAG, chunking, embeddings, vector search, or grounding a model in their documents. Not for prompt wording alone or no-code knowledge-file attachment."
---

# RAG pipeline designer

Grounded in *The AI-Native Engineer*, Part IV. Retrieval quality dominates answer quality — a
pipeline fails silently at ingestion far more often than at generation. Debug in pipeline order.

## Decide whether you need RAG at all

Small stable corpus that fits in context → just load it. Structured records → SQL, not vectors.
Documents attached to a Claude Project or Custom GPT → no-code RAG is enough. Build a pipeline when
the corpus is large, changing, or must produce citations.

## The canonical pipeline

`parse → chunk → embed → store → retrieve → rerank → synthesise → evaluate`

Each stage can destroy the next stage's ceiling. A bad parse cannot be recovered by a better model.

## Procedure

1. **Characterise the corpus first.** Size, formats, structure (headed vs flat), update rate, language
   mix, and whether an answer lives in one chunk or must be assembled across documents. Multi-hop
   corpora need a different retrieval design; you cannot patch that later with prompting.
2. **Parse before you chunk, and check the parse.** Read a sample of extracted text. PDFs lose tables,
   headers and column order; slide decks lose reading order. Silent extraction loss is the most
   common root cause of "RAG doesn't work".
3. **Chunk on structure, with size as a cap, not the rule.** Split at headings and semantic
   boundaries. Add **overlap** so a fact spanning a boundary survives in at least one chunk. Every
   chunk carries its ancestor headings, source file and section anchor in its own text, so hits are
   self-describing and citable.
4. **Embed with retrieval symmetry.** Query and corpus must share the same embedding model *and
   version* to be comparable. Changing the model means reindexing everything — treat the model
   version as part of the index identity. Higher dimensions cost storage and latency for often modest
   gain; measure rather than assume.
5. **Retrieve hybrid by default.** Dense vectors miss exact identifiers — part numbers, register
   names, API symbols; BM25 misses paraphrase. Fuse both, then rerank with a cross-encoder. Technical
   corpora lean more lexical than practitioners expect; test the ratio.
6. **Synthesise under a grounding contract.** Pass chunks with visible source labels, require a
   citation per claim, and require an explicit "not in the provided context" answer. An unanswerable
   question must produce a refusal, not a synthesis.
7. **Evaluate retrieval separately from generation.** Build a question set with known gold chunks and
   track recall@k and MRR *before* touching the prompt. Only then score answers. Tuning the prompt to
   fix a retrieval miss is wasted work.
8. **Plan freshness and deletion.** Define reindex triggers and how a deleted source stops being
   cited. Stale confident citations are the worst production failure mode.

## Debug ladder — stop at the first layer that fails

| Symptom | Check | Typical fix |
|---|---|---|
| Answer omits a known fact | Is the fact in the extracted text at all? | Parser or loader |
| Fact present, chunk never retrieved | Is the gold chunk in top-k? | Chunking, overlap, hybrid retrieval |
| Right chunk retrieved, ignored | Position and labelling in the prompt | Rerank; cut k; label sources |
| Good on some queries, bad on identifiers | Dense-only retrieval | Add lexical/BM25 |
| Confident wrong answer | Is refusal behaviour specified? | Unanswerable instruction + examples |
| Fabricated citation | Are chunk anchors visible and required? | Require verbatim source anchors |
| Worked, now broken | Embedding model changed? | Retrieval symmetry — reindex |
| Degrades over time | Index freshness | Reindex trigger, delete propagation |

## Output format

Corpus profile → parse check → chunking rule with overlap → embedding model and index → retrieval and
rerank configuration → grounding contract → evaluation plan → freshness policy → `Open questions`.

Never claim a specific embedding model is "best" from memory: name candidates, state the trade-off
axes, and mark version-specific claims `UNVERIFIED`. Example metrics are `SYNTHETIC EXAMPLE`.
