import numpy
import pyNN.spiNNaker as pynn


# helper function for populations
def get_pops(n_in_pop, n_used_neuronblocks=7):
    l = []
    model_type = pynn.IF_cond_exp

    for _ in xrange(n_used_neuronblocks):
        pop = pynn.Population(n_in_pop, model_type, params)
        pop.record()
        l.append(pop)

    return l

pynn.setup(timestep=1.0)

duration = 1 * 30000  # ms

params = {
    'cm': 0.2,
    'v_reset': -70,
    'v_rest': -50,
    'v_thresh': -47,
    'e_rev_I': -60,
    'e_rev_E': -40,
}


n_in_pop = 12

# prepare populations
all_pops = []
all_pops.extend(get_pops(n_in_pop))
all_pops.extend(get_pops(n_in_pop))
# -> makes 14 population

# synaptic weight
w_exc = 0.004

con_alltoall = pynn.AllToAllConnector(weights=w_exc * 4)
con_fixednumberpre = pynn.FixedNumberPreConnector(n=4, weights=w_exc)

# stimulate the first population with a single spike (3 times)
spike_times = [0, 1000, 2000]
in_0 = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times': spike_times})

pynn.Projection(in_0, all_pops[0], con_alltoall, target="excitatory")


def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

# connect all populations, but don't close the chain
for pop_a, pop_b in zip(all_pops, shift(all_pops, 1)[:-1]):
    pynn.Projection(pop_a, pop_b, con_fixednumberpre, target='excitatory')

pynn.run(duration)

spikes = None

# Collect and record spikes
for pop in all_pops:
    new_spikes = pop.getSpikes(compatible_output=True)
    if new_spikes is not None:
        numpy.fliplr(new_spikes)
        new_spikes = new_spikes / [1, 1000.0]
        if spikes is None:
            spikes = new_spikes
        else:
            new_spikes = new_spikes + [len(spikes), 0]
            spikes = numpy.concatenate((spikes, new_spikes), axis=0)
if spikes is None:
    spikes = []

print "N spikes", len(spikes)

numpy.savetxt("spikes.dat", spikes)

pynn.end()
