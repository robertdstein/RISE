To include electron resampling, use the pidtool.py present here, rather than the original from Igor and Konstantin's code.

Instructions for installation are found at https://github.com/e5-tu-do/lhcb_pid_resample

Resampling works best if the variables have been transformed first, using a log(var_ProbNNv/(1-var_ProbNNv)) transformation

A code to create a new tree with this branch can be found in this repository at /addbranch/addallprobnn.py

The new branches shall be named with the convention var_newProbNNvar.

The pidtool.py will then read from this branch for resampling.

The branch should also be added to the original downloaded root files.
Copies of the root files can be found at /fhgfs/users/kschubert/public/robert.

At present, only Electron Muon and Kaon branches work.

The sampling binning has not been fine-tuned by me yet. It can be found in line 140 of pidtool.py.

Once this is complete, the root files and the config file pidconfig.json will allow resampling of the branches.