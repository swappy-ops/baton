import os
import sys
# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baton.retrieval.pipeline import get_retrieval_pipeline

def ingest_docs(docs_dir="./docs"):
    pipeline = get_retrieval_pipeline()
    documents = []
    metadatas = []
    ids = []
    
    for filename in os.listdir(docs_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r") as f:
                content = f.read()
                documents.append(content)
                metadatas.append({"source": filename})
                ids.append(filename)
                
    if documents:
        pipeline.add_documents(documents, metadatas, ids)
        print(f"Ingested {len(documents)} documents.")
    else:
        print("No documents found.")

if __name__ == "__main__":
    ingest_docs()
