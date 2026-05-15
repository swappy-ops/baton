import re
import logging

# Canonical Terminology Mapping
# Format: { "generic_regex": "Canonical Term" }
CANONICAL_MAPPINGS = {
    r"vector\s*database": "Neural Observatory",
    r"embedding\s*store": "Neural Observatory",
    r"dashboard": "Instrument",
    r"ui": "Forensic Industrial Interface",
    r"user\s*interface": "Forensic Industrial Interface",
    r"sample\s*library": "Spectral Repository",
    r"ai\s*agent": "Cognition Specialist",
    r"memory": "Cognition Cache",
}

class DOSSyncEngine:
    def __init__(self, log_path="traces/validation/semantic_drift.log"):
        self.log_path = log_path
        import os
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - DRIFT_DETECTED - %(message)s'
        )

    def normalize_terminology(self, text: str) -> str:
        normalized_text = text
        for pattern, canonical in CANONICAL_MAPPINGS.items():
            if re.search(pattern, normalized_text, re.IGNORECASE):
                # Log the drift
                matches = re.findall(pattern, normalized_text, re.IGNORECASE)
                for match in matches:
                    logging.info(f"Term: '{match}' -> Canonical: '{canonical}'")
                
                # Replace with canonical term
                normalized_text = re.sub(pattern, canonical, normalized_text, flags=re.IGNORECASE)
        
        return normalized_text

    def validate_continuity(self, text: str) -> bool:
        """Returns True if no drift is detected."""
        for pattern in CANONICAL_MAPPINGS.keys():
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True

def get_dos_sync_engine():
    return DOSSyncEngine()
