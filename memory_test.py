from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

emb = model.encode(
    "Baton remembers context"
)

print(len(emb))
