"""Run from repository root: python scripts/run_event_robustness.py."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research.event_robustness import audit, read_events

root = Path(__file__).resolve().parents[1]
result = audit(read_events(root / "outputs/per_transit_depths.csv"))
result["source"] = "outputs/per_transit_depths.csv (11 TESS Sector 41 events)"
print(json.dumps(result, indent=2))
