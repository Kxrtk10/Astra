import os
from sentence_transformers import SentenceTransformer

# force huggingface to use local project cache
os.environ["HF_HOME"] = "./model_cache"

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./model_cache"
)


def generate_embedding(text):

    embedding = model.encode(text)

    return embedding.tolist()