"""Optional figure: python scripts/plot_event_robustness.py output.png."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research.event_robustness import audit, read_events

import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
events = read_events(root / "outputs/per_transit_depths.csv")
result = audit(events)
fig, ax = plt.subplots(figsize=(8.5, 4.3))
ax.plot([e[0] for e in events], [e[1]*100 for e in events], "o", label="TESS Sector 41 events")
ax.axhline(result["depth"]["median_depth"]*100, linestyle="--", label="Event median")
lo, _, hi = result["depth"]["bootstrap_16_50_84"]
ax.axhspan(lo*100, hi*100, alpha=0.13, label="Conditional event-bootstrap 68%")
ax.set(xlabel="Transit event index (orbital cycles)", ylabel="Locally normalized depth (%)",
       title="HD 189733 b: event-to-event depth sensitivity")
ax.legend()
fig.tight_layout()
fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "event_robustness.png", dpi=170)
