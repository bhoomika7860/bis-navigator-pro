# BIS Navigator Pro

AI-powered system to recommend BIS standards from product descriptions using RAG (Retrieval-Augmented Generation).

## Features
- Semantic search using embeddings
- Reranking using cross-encoder
- Fast inference pipeline
- JSON-based evaluation system

## How to Run

pip install -r requirements.txt

python inference.py --input test_input.json --output results.json