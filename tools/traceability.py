"""Requirement -> test traceability matrix with pass/fail from the reference run. Writes docs/traceability.md"""
import csv
from model.cruise_ref import CruiseRef, Inputs
from tests.scenarios import SCENARIOS
res = {}
for tc, (reqs, steps) in SCENARIOS.items():
    m = CruiseRef(); res[tc] = all(m.step(Inputs(**i)) == e for i, e in steps)
reqs = list(csv.DictReader(open("requirements/requirements.csv")))
lines = ["| Requirement | Verified by | Result |", "|---|---|---|"]
for r in reqs:
    tcs = r["verification"].split(";")
    ok = all(res[t] for t in tcs); lines.append(f"| {r['req_id']} | {', '.join(tcs)} | {'PASS' if ok else 'FAIL'} |")
uncovered = [r["req_id"] for r in reqs if not r["verification"]]
open("docs/traceability.md", "w").write("# Requirements Traceability Matrix\n\n" + "\n".join(lines) + f"\n\nUncovered requirements: {uncovered or 'none'}\n")
print("\n".join(lines))
