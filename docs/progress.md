# Enterprise Knowledge Assistant — Engineering Progress

This document tracks the RAG system's implementation, experiments, decisions, observations, and next steps. Update this file whenever the project makes a meaningful engineering decision or completes a test cycle.

## 1. Project Goal

Build an enterprise knowledge assistant that ingests documents, retrieves relevant knowledge using semantic search, and generates grounded answers with an LLM.

Current backend stack:

- FastAPI
- PyMuPDF for PDF text extraction
- LangChain RecursiveCharacterTextSplitter for chunking
- Sentence Transformers with `BAAI/bge-small-en-v1.5`
- ChromaDB for vector storage
- Ollama with `qwen3:8b` through the OpenAI-compatible API
- Modular service-oriented backend

## 2. Current End-to-End Flow

```text
User Question
    ↓
Chat API
    ↓
ChatService
    ↓
Conversation History
    ↓
Query Rewriting (for follow-ups)
    ↓
RetrievalService
    ↓
Question Embedding
    ↓
ChromaDB Similarity Search
    ↓
Distance Filtering
    ↓
Top-2 Retrieved Chunks
    ↓
PromptService
    ↓
LLMService / Qwen 3
    ↓
Grounded Answer
    ↓
Sources Returned to User
```

Document ingestion flow:

```text
PDF Upload
    ↓
PyMuPDF Text Extraction
    ↓
Recursive Character Chunking
    ↓
Sentence Transformer Embeddings
    ↓
ChromaDB
```

## 3. Initial RAG Implementation

The backend was implemented as separate services for document processing, chunking, embeddings, vector storage, retrieval, prompt construction, LLM interaction, conversation memory, and query rewriting.

Current chunking configuration:

- chunk size: `1200`
- chunk overlap: `150`
- separators: paragraph, newline, sentence, space, character

Current embedding configuration:

- model: `BAAI/bge-small-en-v1.5`
- normalized embeddings
- dimension observed: `384`

Current LLM configuration:

- model: `qwen3:8b`
- served locally through Ollama
- temperature: `0.2`

## 4. Retrieval Experiments

### 4.1 Initial Retrieval

The first retrieval implementation used vector similarity search with a small number of retrieved chunks. Manual testing showed that relevant questions generally returned semantically relevant chunks.

### 4.2 `top_k` Decision

`top_k` was changed from `3` to `2` after testing.

Reason:

- For the LLM-vs-RAG question, the third retrieved chunk was unnecessary/noisy.
- The answer remained correct with the top two chunks.
- A second test about the role of the LLM also remained good with two chunks.

Decision:

> Keep `top_k = 2` for now. Do not increase it until evaluation shows that useful information is being missed.

This is an experimental choice, not a permanent architectural rule.

### 4.3 Distance Threshold Decision

A maximum retrieval distance was introduced and empirically changed from `0.9` to `0.7`.

Observed behavior:

- Relevant questions commonly produced best distances around `0.51–0.65`.
- Clearly unrelated questions produced distances above `0.7`.
- A supervised-vs-unsupervised-learning query produced a best distance around `0.72` and was rejected.

Decision:

> Keep `MAX_DISTANCE = 0.7` for the current baseline.

Again, this is a measured heuristic and should be revisited with broader evaluation.

## 5. Retrieval Baseline Evaluation

A separate evaluation harness was introduced so that retrieval and generation can be tested without changing production RAG behavior.

Evaluation files:

```text
backend/evaluation/
├── test_cases.json
├── retrieval_eval.py
└── results/
```

The evaluator records:

- test question
- category
- expected topic
- top-k configuration
- retrieved rank
- similarity distance
- chunk number
- source document
- retrieved chunk text
- generated LLM answer
- evaluation configuration
- timestamp

The evaluator deliberately does **not** automatically decide whether a chunk is relevant yet. The first goal is to collect evidence and understand failure patterns before introducing automated scoring.

## 6. Evaluation Dataset

Current baseline contains 10 cases:

- 5 direct/in-document questions
- 3 multi-chunk questions
- 2 out-of-domain questions

Representative tests include:

- What does an LLM do?
- What is cosine similarity?
- Why are embeddings needed in RAG?
- What is chunking and why is it needed?
- What is the difference between fine-tuning and RAG?
- What is the difference between an LLM and RAG?
- Why do we need an LLM instead of just returning the retrieved chunks?
- How does cosine similarity help determine which document is relevant?
- What is the difference between supervised and unsupervised learning?
- What is the capital of France?

## 7. Baseline Findings

### Direct retrieval

For `What does an LLM do?`:

- rank 1: chunk 9, distance approximately `0.515`
- rank 2: chunk 10, distance approximately `0.574`
- both chunks were relevant
- generated answer was well formed and consistent with the retrieved context

### Multi-chunk retrieval

For `What is the difference between an LLM and RAG?`:

- rank 1: chunk 9, distance approximately `0.530`
- rank 2: chunk 10, distance approximately `0.589`
- both were useful for answering the question
- top-2 was sufficient for this test

For `Why do we need an LLM instead of just returning the retrieved chunks?`:

- rank 1: chunk 10, distance approximately `0.499`
- rank 2: chunk 3, distance approximately `0.609`
- rank 1 was strongly relevant
- rank 2 was only partially relevant/noisier
- answer was useful, but contained some reasonable extrapolation beyond the exact retrieved wording

For `How does cosine similarity help determine which document is relevant?`:

- rank 1: chunk 2, distance approximately `0.514`
- rank 2: chunk 3, distance approximately `0.598`
- retrieval found the correct cosine-similarity material
- the source did not fully explain the complete document-ranking process, so the LLM filled in some conceptual detail

### Out-of-domain retrieval

For both:

- `What is the difference between supervised and unsupervised learning?`
- `What is the capital of France?`

retrieval returned an empty result set after the `0.7` distance threshold, and the LLM returned the configured refusal:

`I couldn't find that information in the provided documents.`

This is a strong positive signal for the current threshold.

## 8. Current Assessment

The baseline has **not yet demonstrated a clear retrieval failure**.

Current observations:

- relevant questions generally retrieve useful chunks
- top-2 has been sufficient for the tested examples
- the `0.7` threshold successfully rejects tested out-of-domain questions
- some retrieved second chunks are noisy, but this has not yet caused a major answer failure
- generation sometimes adds reasonable conceptual inference beyond the exact wording of the retrieved chunks

Therefore, the project should not add reranking or increase `top_k` merely because those are common RAG techniques. Changes should be driven by evaluation evidence.

## 9. Current Hypotheses

### Retrieval hypothesis

Current retrieval may already be adequate for straightforward questions. Harder or more varied evaluation cases are needed before changing the retrieval algorithm.

### Generation/grounding hypothesis

The next likely weakness is whether the LLM makes claims that are not directly supported by retrieved context, even when retrieval itself is correct.

## 10. Next Planned Work

1. Finish analyzing the 10-case retrieval baseline.
2. Test grounding/generation behavior using the same stored retrieval evidence.
3. Identify whether unsupported claims are a repeatable problem.
4. Only then decide whether to improve prompting, context construction, answer validation, retrieval, or reranking.
5. Keep the evaluation harness so every future RAG change can be compared against the same baseline.

## 11. Engineering Principle

The project follows an experiment-driven approach:

```text
Observe
  ↓
Form a hypothesis
  ↓
Design a small test
  ↓
Run the test
  ↓
Inspect evidence
  ↓
Make one targeted change
  ↓
Retest against the baseline
```

No optimization should be added without a demonstrated problem or a measurable hypothesis.
