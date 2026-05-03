import chromadb
from context.context_embeddings import generate_embedding

client = chromadb.Client()

collection = client.get_or_create_collection("learning_context")


def store_embedding(text):

    embedding = generate_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[text]
    )


def search_similar(query, k=3):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]