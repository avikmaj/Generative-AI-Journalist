# RAG pipeline design review

Expected skill: `rag-pipeline-designer`. Expected mode: `[GENAI]`.

```text
Review or design this retrieval pipeline.

Corpus: <SIZE, FORMAT, UPDATE FREQUENCY>
Queries look like: <THREE REAL EXAMPLES>
Current design: <CHUNKING, EMBEDDING, STORE, RERANK, PROMPT> or "none yet"
Failure observed: <WRONG ANSWERS, MISSED DOCS, HALLUCINATION, LATENCY>

Return:
1. The design as a table: stage, choice, why, and what it costs.
2. The specific failure mode your change targets, and how you would measure the improvement.
3. The grounding contract: what the generator may assert, and what it must refuse or attribute.
4. Retrieval evaluation set-up: how you would build a labelled set for this corpus.

Do not recommend a vector store by brand without stating the requirement that selects it. Label any
benchmark number or model context limit UNVERIFIED unless sourced.
```

## Why it is shaped this way

RAG advice degenerates into a parts list. Requiring a measurable target per change, and a grounding
contract, keeps the design tied to the observed failure.
