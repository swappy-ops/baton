import os
import json
from datetime import datetime
from projskep.runtime.dos_sync import get_dos_sync_engine

def validate_project_continuity(root_dir=".", audit_id=None):
    sync_engine = get_dos_sync_engine()
    drift_count = 0
    suggestions = []
    
    if not audit_id:
        audit_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    print(f"--- FORENSIC CONTINUITY VALIDATION [{audit_id}] ---")
    
    for root, dirs, files in os.walk(root_dir):
        if any(d.startswith(".") or d == "venv" or d in ["__pycache__", "traces", "embeddings"] for d in root.split(os.sep)):
            continue
            
        for file in files:
            if file.endswith((".py", ".md", ".json")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        if not sync_engine.validate_continuity(content):
                            normalized = sync_engine.normalize_terminology(content)
                            suggestions.append({
                                "file": filepath,
                                "type": "terminology_drift",
                                "proposal": normalized
                            })
                            drift_count += 1
                            
                        # Check for chunk fragmentation in markdown
                        if file.endswith(".md") and "Neural Observatory" in content:
                            if len(content.split()) < 20:
                                print(f"Chunk Quality Alert: {filepath} (Too sparse)")
                except Exception as e:
                    pass

    # Log suggestions to traces/audits/
    audit_file = f"traces/audits/{audit_id}.json"
    os.makedirs(os.path.dirname(audit_file), exist_ok=True)
    
    audit_report = {
        "audit_id": audit_id,
        "timestamp": datetime.now().isoformat(),
        "drift_count": drift_count,
        "suggestions": suggestions
    }
    
    with open(audit_file, "w") as f:
        json.dump(audit_report, f, indent=2)

    distilled_count = len([f for f in os.listdir("./memory/distilled") if f.endswith(".md")])
    print(f"\n--- SEMANTIC REPOSITORY STATUS ---")
    print(f"Distilled Artifacts: {distilled_count}")
    print(f"Validation Complete. Total Drift Events: {drift_count}")
    print(f"SUGGESTION REPORT: {audit_file}")
    
    return audit_file

if __name__ == "__main__":
    validate_project_continuity()
