import json
import time
import argparse
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

# load models
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# create DB
client = chromadb.Client()
collection = client.create_collection("bis_standards")

# TEMP DATA (replace later with Person D data)
import json

with open("corpus.json", "r") as f:
    data = json.load(f)

documents = [item["text"] for item in data]
ids = [item["standard_id"] for item in data]

collection.add(documents=documents, ids=ids)


def retrieve(query):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    docs = results["documents"][0]

    # rerank
    pairs = [(query, doc) for doc in docs]
    scores = reranker.predict(pairs)

    reranked = list(zip(ids, docs, scores))
    reranked = sorted(reranked, key=lambda x: x[2], reverse=True)

    # return top 3 IDs
    return [r[0] for r in reranked[:3]]


def main(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)

    output = []

    for item in data:
        start = time.time()

        query = item["query"]
        results = retrieve(query)

        end = time.time()

        output.append({
            "id": item["id"],
            "retrieved_standards": results,
            "latency_seconds": round(end - start, 3)
        })

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()
    main(args.input, args.output)