"""Core Canary Memory Sentinel implementation."""
import hashlib
import secrets
import time
from typing import Dict, Any, Optional

class CanaryRecord:
    def __init__(self, canary_id: str, secret_token: str, context_tag: str):
        self.canary_id = canary_id
        self.secret_token = secret_token
        self.context_tag = context_tag
        self.created_at = time.time()

class CanaryMemorySentinel:
    def __init__(self, master_key: str = "sentinel-secret"):
        self.master_key = master_key
        self.active_canaries: Dict[str, CanaryRecord] = {}

    def plant_canary(self, context_tag: str) -> str:
        canary_id = f"canary_{secrets.token_hex(4)}"
        secret = hashlib.sha256(f"{self.master_key}:{canary_id}:{context_tag}".encode("utf-8")).hexdigest()[:16]
        self.active_canaries[canary_id] = CanaryRecord(canary_id, secret, context_tag)
        return f"<!-- CANARY:{canary_id}:{secret} -->"

    def inspect_memory(self, memory_text: str) -> Dict[str, Any]:
        tampered = []
        found_count = 0
        for cid, rec in self.active_canaries.items():
            expected = f"<!-- CANARY:{cid}:{rec.secret_token} -->"
            if expected in memory_text:
                found_count += 1
            else:
                # check if partial exists (tampered)
                if f"<!-- CANARY:{cid}" in memory_text:
                    tampered.append(cid)

        return {
            "intact": len(tampered) == 0,
            "found_canaries": found_count,
            "tampered_canaries": tampered
        }
