% UNTESTED helper - adjust names to your model. Runs stimulus.csv through CruiseCtrl.slx and exports mil_out.csv
T = readtable('data/stimulus.csv');
in = [T.t, T.enable, T.set_sw, T.resume_sw, T.brake, T.clutch, T.speed];   % one column per root Inport, in order
simIn = Simulink.SimulationInput('CruiseCtrl');
ds = Simulink.SimulationData.Dataset;   % or use From Workspace blocks with timeseries(in(:,2:end), in(:,1))
% Reset state per test case: Stateflow resets if you gate each TC with a reset signal, or run one sim per TC.
% Log outputs state,set_speed,cc_active as signal logging, then:
% writetable(table(T.t, T.tc, state, set_speed, cc_active, 'VariableNames', {'t','tc','state','set_speed','cc_active'}), 'data/mil_out.csv');
