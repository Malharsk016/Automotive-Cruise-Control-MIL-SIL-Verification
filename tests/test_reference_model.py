import pytest
from model.cruise_ref import CruiseRef, Inputs
from tests.scenarios import SCENARIOS

@pytest.mark.parametrize("tc", SCENARIOS)
def test_scenario(tc):
    reqs, steps = SCENARIOS[tc]
    m = CruiseRef()
    for k, (inp, exp) in enumerate(steps):
        assert m.step(Inputs(**inp)) == exp, f"{tc} ({reqs}) step {k}"
