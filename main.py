import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder

# load models
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# create database
client = chromadb.Client()
collection = client.create_collection("bis_standards")

# sample data
documents = [
    "IS 1786 steel reinforcement bars used in construction",
    "IS 456 code for plain and reinforced concrete",
    "IS 269 specification for ordinary portland cement"
]

ids = ["IS1786", "IS456", "IS269"]

collection.add(documents=documents, ids=ids)

# query
queries = [
    "steel rods for building",
    "cement for construction",
    "concrete mix for house"
]

for query in queries:
    results = collection.query(
        query_texts=[query],
         n_results=10
    )

    docs = results["documents"][0]

    # rerank
    pairs = [(query, doc) for doc in docs]
    scores = reranker.predict(pairs)

    reranked = list(zip(docs, scores))
    reranked = sorted(reranked, key=lambda x: x[1], reverse=True)

    print("\n======================")
    print("Query:", query)
    print("Top Results:")

    for doc, score in reranked:
        print(f"{doc} (score: {score:.4f})")