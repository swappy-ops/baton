import chromadb
import json
import time
from datetime import datetime
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os

class RetrievalQualityScorer:
    def __init__(self, trace_dir="traces/retrieval"):
        self.trace_dir = trace_dir
        os.makedirs(trace_dir, exist_ok=True)

    def log_hit_rate(self, query: str, results: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_file = os.path.join(self.trace_dir, f"hits_{timestamp}.json")
        
        hit_data = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "results_count": len(results.get("documents", [])),
            "top_score": results.get("scores", [0])[0] if results.get("scores") else 0,
            "mean_score": sum(results.get("scores", [])) / len(results.get("scores")) if results.get("scores") else 0
        }
        
        with open(trace_file, "w") as f:
            json.dump(hit_data, f, indent=2)

class RetrievalPipeline:
    def __init__(self, db_path="./embeddings/chroma"):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("projskep_docs")
        self.scorer = RetrievalQualityScorer()

    def add_documents(self, documents: list, metadatas: list, ids: list):
        embeddings = self.model.encode(documents).tolist()
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 5):
        query_embedding = self.model.encode([query_text]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        diagnostics = self._run_diagnostics(results)
        scored_results = self._score_results(results, diagnostics)
        
        # Log quality metrics
        self.scorer.log_hit_rate(query_text, scored_results)
        
        return scored_results

    def _run_diagnostics(self, results):
        docs = results.get('documents', [[]])[0]
        distances = results.get('distances', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        
        stale_threshold = time.time() - (30 * 24 * 60 * 60) # 30 days
        stale_count = 0
        for meta in metadatas:
            if meta and 'timestamp' in meta:
                if meta['timestamp'] < stale_threshold:
                    stale_count += 1
        
        diagnostics = {
            "duplicate_count": len(docs) - len(set(docs)),
            "relevance_scores": [1.0 - d for d in distances],
            "noise_threshold_met": any((1.0 - d) < 0.4 for d in distances),
            "stale_count": stale_count,
            "redundancy_alert": False
        }
        
        if stale_count > 0:
            print(f"DIAGNOSTIC: Detected {stale_count} stale memory chunks.")
            
        return diagnostics

    def _score_results(self, results, diagnostics):
        scores = [self._compute_score(relevance, diagnostics["noise_threshold_met"], diagnostics["redundancy_alert"])
                   for relevance in diagnostics["relevance_scores"]]

        return {"documents": results.get("documents")[0] if results.get("documents") else [],
                "distances": results.get("distances")[0] if results.get("distances") else [],
                "scores": scores,
                "diagnostics": diagnostics}

    def _compute_score(self, relevance, noise_threshold_met, redundancy_alert):
        score = relevance
        if noise_threshold_met:
            score -= 0.1
        if redundancy_alert:
            score -= 0.2

        return max(score, 0)

def get_retrieval_pipeline():
    return RetrievalPipeline()
