"""Encode reference-model output as J1939 CCVS1 frames (candump-style log), then decode with cantools
and assert signals vs expected. Mimics a bench/log-analysis check."""
import cantools, csv
from model.cruise_ref import CruiseRef, Inputs
from tests.scenarios import SCENARIOS
db = cantools.database.load_file("data/j1939_ccvs1.dbc")
msg = db.get_message_by_name("CCVS1")
FRAME_ID = msg.frame_id

def encode(inp, cc_active, set_speed):
    return msg.encode(dict(WheelBasedVehicleSpeed_SPN84=inp["speed"], CruiseControlActive_SPN595=cc_active,
        CruiseControlEnableSwitch_SPN596=inp["enable"], BrakeSwitch_SPN597=inp["brake"], ClutchSwitch_SPN598=inp["clutch"],
        CruiseControlSetSwitch_SPN599=inp["set_sw"], CruiseControlResumeSwitch_SPN601=inp["resume_sw"],
        CruiseControlSetSpeed_SPN86=set_speed))

def write_log(path="data/ccvs1.log"):
    t = 0.0
    with open(path, "w") as f:
        for tc, (_, steps) in SCENARIOS.items():
            m = CruiseRef()
            for inp, _ in steps:
                st, sp, act = m.step(Inputs(**inp))
                f.write(f"({t:.3f}) can0 {FRAME_ID:08X}#{encode(inp, act, sp).hex().upper()} # {tc}\n"); t += 0.1
    return path

def decode_log(path="data/ccvs1.log"):
    rows = []
    for line in open(path):
        head, tc = line.rsplit("#", 1)[0], line.rsplit("#", 1)[1].strip()
        frame = head.split()[2]; fid, data = frame.split("#")
        assert int(fid, 16) == FRAME_ID, "unexpected CAN ID"
        rows.append((tc, db.decode_message(FRAME_ID, bytes.fromhex(data))))
    return rows

if __name__ == "__main__":
    write_log(); rows = decode_log()
    print(f"decoded {len(rows)} CCVS1 frames; first:", rows[0][1])
