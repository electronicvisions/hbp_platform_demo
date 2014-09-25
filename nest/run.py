import sys, os

backend = 'nest'
if len(sys.argv) != 2:
    print 'provide PyNN backend as argument, e.g. nest, hardware.stage1 etc'
    exit()
else:
    backend = sys.argv[1]
exec('import pyNN.' + backend + ' as pynn')

import numpy as np
import numpy.random as rng
import matplotlib.pyplot as plt

runtime = 300.0
noPops = 11
popSize = {'exc': 8, 'inh': 8}
weightExcExc = 0.02
weightExcInh = 0.02
weightInhExc = 0.2
delay = 3.0
stimulusOnset = 25.0
stimulusSigma = 0.5
rng_seed = 42

pynn.setup()

#create synfire populations
popCollector = {'exc': [], 'inh': []}
for popIndex in range(noPops):
    for synType in ['exc', 'inh']:
        pop = pynn.Population(popSize[synType], pynn.IF_cond_exp)
        pop.record()
        popCollector[synType].append(pop)

#connect synfire chain
connectorExcExc = pynn.AllToAllConnector(weights=weightExcExc, delays=delay)
connectorExcInh = pynn.AllToAllConnector(weights=weightExcInh, delays=delay)
connectorInhExc = pynn.AllToAllConnector(weights=weightInhExc, delays=delay)
for sourcePop in range(noPops):
    targetPop = (sourcePop + 1) % noPops

    pynn.Projection(popCollector['exc'][sourcePop], popCollector['exc'][targetPop],
                    connectorExcExc, target='excitatory')
    pynn.Projection(popCollector['exc'][sourcePop], popCollector['inh'][targetPop],
                    connectorExcInh, target='excitatory')
    pynn.Projection(popCollector['inh'][sourcePop], popCollector['exc'][sourcePop],
                    connectorInhExc, target='inhibitory')

#create stimulus
rng.seed(rng_seed)
stimulus = pynn.Population(popSize['exc'], pynn.SpikeSourceArray)
stimSpikes = rng.normal(loc=stimulusOnset, scale=stimulusSigma, size=popSize['exc'])

for i, oneStimulus in enumerate(stimulus):
    oneStimulus.set_parameters(spike_times=[stimSpikes[i]])

#connect stimulus
pynn.Projection(stimulus, popCollector['exc'][0], connectorExcExc, target='excitatory')
pynn.Projection(stimulus, popCollector['inh'][0], connectorExcInh, target='excitatory')

#run simulation/emulation
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
plt.savefig('result.png')

pynn.end()
