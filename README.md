# Truck Cruise Control ECU Function: MIL-to-SIL Back-to-Back Verification with J1939 Analysis

Model-based development and verification workflow on a small automotive function (cruise control state machine), following an ASPICE-style flow: requirement -> design -> test -> traceability.

## Contents
- `requirements/requirements.csv` - 10 written requirements (REQ-CC-001..010)
- `model/cruise_ref.py` - Python reference model (executable spec)
- `tests/scenarios.py` - 8 requirement-tagged test cases (TC-01..TC-08); `tests/test_*.py` - pytest
- `tools/make_stimulus.py` - exports `data/stimulus.csv` + `data/expected_ref.csv` for the Simulink/Stateflow model
- `tools/b2b_compare.py` - back-to-back comparator (reference vs MIL or SIL output CSV)
- `tools/can_log.py` + `data/j1939_ccvs1.dbc` - J1939 CCVS1 (PGN 65265) encode/decode with cantools, signal checks
- `tools/traceability.py` -> `docs/traceability.md`
- `model/CruiseCtrl.slx` - Simulink/Stateflow model (built in MATLAB; see docs/build_guide.md)

## Run
    pip install cantools python-can pytest pandas
    export PYTHONPATH=.
    python -m tools.make_stimulus && python -m tools.traceability && pytest
    python tools/b2b_compare.py data/mil_out.csv    # after exporting from Simulink
    python tools/b2b_compare.py data/sil_out.csv    # after SIL run of generated C

## Status
- [x] Requirements, reference model, tests, J1939 decode, traceability, comparator
- [ ] Simulink/Stateflow model, MIL run, SIL run (Embedded Coder), results in docs/results.md
