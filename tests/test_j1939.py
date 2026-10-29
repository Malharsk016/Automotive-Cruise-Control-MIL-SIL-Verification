import pytest
from tools.can_log import write_log, decode_log
from model.cruise_ref import CruiseRef, Inputs
from tests.scenarios import SCENARIOS

def test_ccvs1_decode_matches_reference(tmp_path):
    p = write_log(str(tmp_path / "ccvs1.log")); rows = decode_log(p)
    expected = []
    for tc, (_, steps) in SCENARIOS.items():
        m = CruiseRef()
        for inp, _e in steps:
            expected.append((tc, inp, m.step(Inputs(**inp))))
    assert len(rows) == len(expected)
    for (tc, sig), (_, inp, (st, sp, act)) in zip(rows, expected):
        assert sig["CruiseControlActive_SPN595"] == act, tc
        assert sig["CruiseControlSetSpeed_SPN86"] == sp, tc
        assert abs(sig["WheelBasedVehicleSpeed_SPN84"] - inp["speed"]) < 0.01, tc
