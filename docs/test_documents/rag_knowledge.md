# Retrieval-Augmented Generation (RAG)

## What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with a generative language model. Instead of relying only on information stored in the model's parameters, RAG retrieves relevant information from an external knowledge source and provides that information to the language model as context.

## What does RAG do?

RAG retrieves relevant information from an external knowledge source and uses the retrieved information as context when generating a response. This allows the application to use information that is stored outside the language model.

## How does RAG work?

A typical RAG pipeline follows these steps:

1. The user submits a question.
2. The question is converted into an embedding.
3. The embedding is compared with embeddings stored in a vector database.
4. The most relevant document chunks are retrieved.
5. The retrieved chunks are provided to the language model as context.
6. The language model generates a response using the retrieved context.

## Does RAG modify the model?

RAG does not modify the language model's parameters or weights during retrieval and generation. The external information is supplied as context at inference time.

## RAG vs Fine-tuning

Fine-tuning changes the model's parameters by training it on additional examples. RAG does not change the model's parameters; instead, it retrieves external information and supplies it as context during generation.

## Why is RAG useful?

RAG is useful when an application needs to answer questions using information stored in external documents or knowledge sources. It allows the retrieval system to provide relevant information to the language model without requiring the model itself to be retrained for every change in the knowledge source.
