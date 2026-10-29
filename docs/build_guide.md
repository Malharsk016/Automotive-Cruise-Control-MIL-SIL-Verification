# Simulink/Stateflow build (about 3 hrs)
1. New model `CruiseCtrl.slx`, fixed-step discrete, Ts = 1 (one step per CSV row). Inports: enable, set_sw, resume_sw, brake, clutch, speed. Outports: state, set_speed, cc_active.
2. Chart with states OFF, STANDBY, ACTIVE, SUSPENDED (state 0..3 to match reference). Local data: prev_set, prev_resume (updated at end of every step). Edge: set_edge = set_sw && !prev_set.
3. Transitions: copy guards from model/cruise_ref.py line by line; annotate each with REQ-CC-xxx in the label comment.
4. Entry/during actions: set_speed latched on STANDBY->ACTIVE (round(speed)); cleared on OFF/STANDBY. cc_active = (state==ACTIVE).
5. Reset per test case: add Inport `rst` (high on first row of each TC) or run one sim per TC and concatenate.
6. MIL: run stimulus.csv, export mil_out.csv with columns t,tc,state,set_speed,cc_active; run b2b_compare.py.
7. SIL: Embedded Coder / SIL mode (or generate C with Simulink Coder and harness it); export sil_out.csv; compare.
8. Commit model, outputs, and docs/results.md (pass/fail table, any defects found and fixed).
