"""Back-to-back comparison: reference expected_ref.csv vs model output CSV (Simulink MIL or SIL).
Usage: python tools/b2b_compare.py data/mil_out.csv   (columns: t,tc,state,set_speed,cc_active)"""
import sys, pandas as pd
ref = pd.read_csv("data/expected_ref.csv")
dut = pd.read_csv(sys.argv[1])
assert len(ref) == len(dut), f"length mismatch ref={len(ref)} dut={len(dut)}"
bad = ref.merge(dut, on=["t"], suffixes=("_ref","_dut"))
mm = bad[(bad.state_ref!=bad.state_dut)|(bad.set_speed_ref!=bad.set_speed_dut)|(bad.cc_active_ref!=bad.cc_active_dut)]
if mm.empty: print(f"PASS: {len(ref)} steps match ({sys.argv[1]})"); sys.exit(0)
print(f"FAIL: {len(mm)} mismatching steps"); print(mm[["t","tc_ref","state_ref","state_dut","set_speed_ref","set_speed_dut"]].to_string(index=False)); sys.exit(1)
