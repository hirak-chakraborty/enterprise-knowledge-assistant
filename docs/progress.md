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

The baseline began with 10 cases. Grounding evaluation subsequently expanded the dataset to 16 cases.

Current categories include:

- direct/in-document questions
- multi-chunk questions
- out-of-domain questions
- grounding-supported questions
- grounding-partial questions
- grounding-insufficient questions
- grounding-unsupported questions

Representative grounding tests include:

- What does an LLM do?
- How does cosine similarity help determine which document is relevant?
- What are the advantages of using GPT-4 over Qwen 3?
- Why does cosine similarity use the angle between vectors instead of their magnitude?
- How does the Transformer attention mechanism improve RAG retrieval?
- What happens if two documents have exactly the same cosine similarity to a query?

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
- before the grounding prompt change, the source did not fully explain the complete document-ranking process, so the LLM filled in some conceptual detail

### Out-of-domain retrieval

For both:

- `What is the difference between supervised and unsupervised learning?`
- `What is the capital of France?`

retrieval returned an empty result set after the `0.7` distance threshold, and the LLM returned the configured refusal:

`I couldn't find that information in the provided documents.`

This is a strong positive signal for the current threshold.

## 8. Grounding Evaluation and Prompt Experiment

A grounding-focused test set was added to determine whether the LLM stays within retrieved evidence or introduces plausible information from outside the context.

### Initial grounding baseline

Three initial cases showed:

- Fully supported question: answered correctly and remained grounded.
- Partially supported question: answer was conceptually reasonable but added information not explicitly stated in the retrieved chunks.
- Unsupported question: correctly refused.

A further stress test was then used to distinguish between related-but-insufficient evidence and fully unsupported questions.

### Grounding failure discovered

For `How does the Transformer attention mechanism improve RAG retrieval?`, retrieval returned chunks containing Transformer, attention, RAG, embeddings, and retrieval-related concepts. However, the retrieved evidence did not explicitly establish that Transformer attention improves RAG retrieval.

Before the prompt change, the LLM nevertheless generated an explanation claiming that attention improves RAG retrieval. This was classified as an unsupported inference/hallucination.

This demonstrated an important distinction:

> Semantic similarity of retrieved chunks does not guarantee that the retrieved evidence is sufficient to answer the question.

### Controlled prompt intervention

Only the generation prompt was changed. Retrieval configuration, embeddings, chunking, `top_k`, distance threshold, and LLM configuration were kept unchanged.

The generation instructions were strengthened to explicitly require:

- answers strictly from the provided context
- no outside knowledge or assumptions
- no unstated relationships between separate facts
- refusal when related context does not directly answer the question
- refusal rather than inference when uncertain

### Retest results

Tests 11–16 were rerun after the prompt change:

- `What does an LLM do?` → still answered correctly.
- `How does cosine similarity help determine which document is relevant?` → became more conservative and refused rather than making an inference not directly supported by the chunks.
- `What are the advantages of using GPT-4 over Qwen 3?` → correctly refused.
- `Why does cosine similarity use the angle between vectors instead of their magnitude?` → correctly refused.
- `How does the Transformer attention mechanism improve RAG retrieval?` → previous unsupported answer was replaced by the correct refusal.
- `What happens if two documents have exactly the same cosine similarity to a query?` → correctly refused.

### Decision

> Keep the stricter grounding prompt for now.

It successfully eliminated the observed unsupported inference in the key stress test while preserving correct behavior on clearly supported questions.

However, the change may be somewhat conservative: the cosine-similarity test moved from a reasonable conceptual answer to a refusal. This should be evaluated later with additional clearly answerable and multi-chunk questions before further prompt tuning.

## 9. Current Assessment

The baseline has **not yet demonstrated a clear retrieval failure**.

Current observations:

- relevant questions generally retrieve useful chunks
- top-2 has been sufficient for the tested examples
- the `0.7` threshold successfully rejects tested out-of-domain questions
- some retrieved second chunks are noisy, but this has not yet caused a major answer failure
- generation previously added reasonable conceptual inference beyond the exact wording of retrieved chunks
- the stricter grounding prompt now makes the generation layer more conservative and prevents the observed unsupported inference case

Therefore, the project should not add reranking or increase `top_k` merely because those are common RAG techniques. Changes should be driven by evaluation evidence.

## 10. Current Hypotheses

### Retrieval hypothesis

Current retrieval may already be adequate for straightforward questions. Harder or more varied evaluation cases are needed before changing the retrieval algorithm.

### Generation/grounding hypothesis

The LLM can be controlled more reliably by explicit grounding constraints, but overly strict instructions may reduce useful answers when the context supports an answer through straightforward synthesis. More evaluation is required before further tuning.

## 11. Next Planned Work

The grounding prompt change is considered a successful first intervention, but the project will temporarily move forward to other system capabilities rather than over-optimize this area immediately.

Planned future grounding work:

1. Add more clearly answerable multi-chunk questions.
2. Measure whether the stricter prompt causes unnecessary refusals.
3. Revisit prompt/context construction only if evaluation shows a meaningful tradeoff.

Other project work can proceed in parallel so that the system continues to grow while this question remains documented for later refinement.

## 12. Engineering Principle

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

The project also deliberately avoids treating AI agents as a black-box replacement for engineering. AI is used as an engineering partner, while architectural decisions, experiments, failure analysis, and implementation reasoning remain understandable and defensible by the project owner.
