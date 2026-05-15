import os
import ast
from projskep.retrieval.pipeline import get_retrieval_pipeline

class StructuralIndexer:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir
        self.pipeline = get_retrieval_pipeline()

    def scan_repo(self):
        print("--- NEURAL OBSERVATORY: STRUCTURAL INDEXING ---")
        for root, dirs, files in os.walk(self.root_dir):
            if any(d.startswith(".") or d == "venv" or d == "__pycache__" for d in root.split(os.sep)):
                continue
                
            for file in files:
                if file.endswith(".py"):
                    self._index_python_file(os.path.join(root, file))

    def _index_python_file(self, filepath):
        rel_path = os.path.relpath(filepath, self.root_dir)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
                
            symbols = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    symbols.append(f"class:{node.name}")
                elif isinstance(node, ast.FunctionDef):
                    symbols.append(f"func:{node.name}")
                    
            # Create a structural summary for retrieval
            summary = f"File: {rel_path}\nSymbols: {', '.join(symbols)}"
            
            self.pipeline.add_documents(
                documents=[summary],
                metadatas=[{"type": "structural_index", "path": rel_path}],
                ids=[f"struct_{rel_path.replace(os.sep, '_')}"]
            )
        except Exception as e:
            print(f"Error indexing {rel_path}: {e}")

def run_structural_indexing():
    indexer = StructuralIndexer()
    indexer.scan_repo()

if __name__ == "__main__":
    run_structural_indexing()
