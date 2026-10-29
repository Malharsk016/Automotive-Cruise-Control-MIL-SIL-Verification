"""Export every scenario as one concatenated stimulus CSV (feed to Simulink via From Workspace / readtable),
plus the expected-output CSV from the Python reference model."""
import csv, pathlib
from model.cruise_ref import CruiseRef, Inputs
from tests.scenarios import SCENARIOS
out = pathlib.Path("data"); out.mkdir(exist_ok=True)
cols = ["t","tc","enable","set_sw","resume_sw","brake","clutch","speed"]
with open(out/"stimulus.csv","w",newline="") as fs, open(out/"expected_ref.csv","w",newline="") as fe:
    ws, we = csv.writer(fs), csv.writer(fe)
    ws.writerow(cols); we.writerow(["t","tc","state","set_speed","cc_active"])
    t = 0
    for tc, (reqs, steps) in SCENARIOS.items():
        m = CruiseRef()                      # fresh model per test case
        for inp, _ in steps:
            st, sp, act = m.step(Inputs(**inp))
            ws.writerow([t, tc] + [inp[c] for c in cols[2:]])
            we.writerow([t, tc, st, sp, act]); t += 1
print("wrote data/stimulus.csv, data/expected_ref.csv")
