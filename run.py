from os import open, close, dup, O_WRONLY, O_CREAT
oldstdout = dup(1)
close(1)
open("stdout", O_WRONLY|O_CREAT)

oldstderr = dup(2)
close(2)
open("stderr", O_WRONLY|O_CREAT)



import os
import sys
import shutil
import plot_spikes
import time


from pyNN.utility import get_script_args
simulator_name = get_script_args(1)[0]

# Warning this can be overwritten by the scrips run by execfile (Hacky, hacky,...)
filename_script = os.path.join(simulator_name, 'run.py')
filename_spikes = 'spikes.dat'
filename_spikes_backup = 'spikes.dat.{}.bak'.format(time.time())
filename_result_plot = 'result.png'

if os.path.isfile(filename_spikes):
    shutil.move(filename_spikes, filename_spikes_backup)

if os.path.isfile(filename_script):
    execfile(filename_script)
else:
    print 'Backend {} not found :('.format(simulator_name)
    exit(1)

if not os.path.isfile(filename_spikes):
    print 'No spike file found :('

plot_spikes.plot(filename_spikes, filename_result_plot)




close(2)
dup(oldstderr) # should dup to 2
close(oldstderr) # get rid of left overs

sys.stdout.flush() # otherwise it will end up on stdout
close(1)
dup(oldstdout) # should dup to 1
close(oldstdout) # get rid of left overs

# tail 'stdout' to stdout
from __builtin__ import open
with open('stdout', 'r') as fd:
        print ''.join(fd.readlines()[-20:]),
