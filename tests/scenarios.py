"""Requirement-tagged scenarios: (requirement ids, [(input dict, expected (state, set_speed, active))])."""
from model.cruise_ref import OFF, STANDBY, ACTIVE, SUSPENDED
def S(enable=1, set_sw=0, resume_sw=0, brake=0, clutch=0, speed=0.0):
    return dict(enable=enable, set_sw=set_sw, resume_sw=resume_sw, brake=brake, clutch=clutch, speed=speed)

SCENARIOS = {
 "TC-01": ("REQ-CC-001;REQ-CC-009", [(S(enable=0,speed=60),(OFF,0,0)), (S(speed=60),(STANDBY,0,0)), (S(enable=0,speed=60),(OFF,0,0))]),
 "TC-02": ("REQ-CC-002;REQ-CC-009", [(S(enable=0),(OFF,0,0)), (S(),(STANDBY,0,0))]),
 "TC-03": ("REQ-CC-003;REQ-CC-010", [(S(),(STANDBY,0,0)), (S(),(STANDBY,0,0)), (S(set_sw=1,speed=80.4),(ACTIVE,80,1)), (S(speed=82),(ACTIVE,80,1))]),
 "TC-04": ("REQ-CC-004;REQ-CC-009", [(S(speed=20),(STANDBY,0,0)), (S(set_sw=1,speed=20),(STANDBY,0,0))]),
 "TC-05": ("REQ-CC-005;REQ-CC-010", [(S(speed=70),(STANDBY,0,0)), (S(set_sw=1,speed=70),(ACTIVE,70,1)), (S(brake=1,speed=69),(SUSPENDED,70,0))]),
 "TC-06": ("REQ-CC-006;REQ-CC-010", [(S(speed=70),(STANDBY,0,0)), (S(set_sw=1,speed=70),(ACTIVE,70,1)), (S(clutch=1,speed=69),(SUSPENDED,70,0)),
                                      (S(speed=69),(SUSPENDED,70,0)), (S(resume_sw=1,speed=69),(ACTIVE,70,1))]),
 "TC-07": ("REQ-CC-007;REQ-CC-009", [(S(speed=70),(STANDBY,0,0)), (S(set_sw=1,speed=70),(ACTIVE,70,1)), (S(speed=25),(STANDBY,0,0))]),
 "TC-08": ("REQ-CC-008", [(S(speed=110),(STANDBY,0,0)), (S(set_sw=1,speed=110),(STANDBY,0,0))]),
}
