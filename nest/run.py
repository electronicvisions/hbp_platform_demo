import sys, os

backend = 'nest'
if len(sys.argv) != 2:
    print 'provide PyNN backend as argument, e.g. nest, hardware.stage1 etc'
    exit()
else:
    backend = sys.argv[1]
exec('import pyNN.' + backend + ' as pynn')

import pyNN.nest as pynn
import numpy as np
import matplotlib.pyplot as plt

runtime = 300.0
noPops = 9
popSize = {'exc': 10, 'inh': 10}

pynn.setup()

weightStimExcExc = 50.0 / 3e3 #10.0 / 3e3
weightStimExcInh = 50.0 / 3e3 #10.0 / 3e3
weightExcExc = 50.0 / 3e3 #5 / 3e3
weightExcInh = 50.0 / 3e3 #10 / 3e3
weightInhExc = 200.0 / 1e3 #15 / 1e3
stimSpikes = np.array([10.0])
delay = 3.0

stimExc = pynn.Population(popSize['exc'], pynn.SpikeSourceArray, {'spike_times': stimSpikes})

popCollector = {'exc': [], 'inh': []}
for synType in ['exc', 'inh']:
    for popIndex in range(noPops):
        pop = pynn.Population(popSize[synType], pynn.IF_cond_exp)
        pop.record()
        popCollector[synType].append(pop)

pynn.Projection(stimExc, popCollector['exc'][0], pynn.AllToAllConnector(weights=weightStimExcExc, delays=delay), target='excitatory')
pynn.Projection(stimExc, popCollector['inh'][0], pynn.AllToAllConnector(weights=weightStimExcInh, delays=delay), target='excitatory')
for popIndex in range(noPops):
    pynn.Projection(popCollector['exc'][popIndex], popCollector['exc'][(popIndex + 1) % noPops],
                    pynn.AllToAllConnector(weights=weightExcExc, delays=delay), target='excitatory')
    pynn.Projection(popCollector['exc'][popIndex], popCollector['inh'][(popIndex + 1) % noPops],
                    pynn.AllToAllConnector(weights=weightExcInh, delays=delay), target='excitatory')
    pynn.Projection(popCollector['inh'][popIndex], popCollector['exc'][popIndex],
                    pynn.AllToAllConnector(weights=weightInhExc, delays=delay), target='inhibitory')

pynn.run(runtime)

plt.figure()
spikeCollector = np.array([]).reshape(0,2)
indexMod = 0
color = 'k'
for synType in ['exc', 'inh']:
    for popIndex in range(noPops):
        if synType == 'exc':
            indexMod = 2 * popIndex * popSize[synType]
            color = 'b'
        elif synType == 'inh':
            indexMod = (2 * popIndex + 1) * popSize[synType]
            color = 'r'
        else:
            assert(True)
        spikes = popCollector[synType][popIndex].getSpikes()
        spikes[:,0] += indexMod
        plt.plot(spikes[:,1], spikes[:,0], ls='', marker='o', ms=1, c=color, mec=color)
        spikeCollector = np.vstack((spikeCollector, spikes))

print 'no spikes:', len(spikeCollector)
np.savetxt('spikes.dat', spikeCollector)

plt.xlim((0, runtime))
plt.ylim((-0.5, noPops * (popSize['exc'] + popSize['inh']) + 0.5))
plt.xlabel('time (t)')
plt.ylabel('neuron index')
plt.savefig('results.png')

pynn.end()
