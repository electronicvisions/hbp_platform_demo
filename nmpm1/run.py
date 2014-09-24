from pyNN.utility import get_script_args
simulator_name = get_script_args(1)[0]

print simulator_name

import numpy as np
import os, sys

# NM-PM1 specific initialisation
if simulator_name == "NM-PM1":

    import pylogging
    import pyhmf as pynn
    from pymarocco import PyMarocco
    from pyhalbe.Coordinate import SynapseDriverOnHICANN, HICANNGlobal, X, Y, Enum,  NeuronOnHICANN
    import Coordinate as C
    import pyhalbe
    import pyredman

    pylogging.set_loglevel(pylogging.get("Default"), pylogging.LogLevel.INFO)
    pylogging.set_loglevel(pylogging.get("marocco"), pylogging.LogLevel.DEBUG)
    pylogging.set_loglevel(pylogging.get("sthal.HICANNConfigurator.Time"), pylogging.LogLevel.DEBUG)

    h = pyredman.Hicann()

    def initBackend(fname):
        lib = pyredman.loadLibrary(fname)
        backend = pyredman.loadBackend(lib)
        if not backend:
            raise Exception('unable to load %s' % fname)
        return backend

    neuron_size = 4

    marocco = PyMarocco()
    marocco.placement.setDefaultNeuronSize(neuron_size)
    marocco.placement.use_output_buffer7_for_dnc_input_and_bg_hack = True
    marocco.placement.minSPL1 = False
    marocco.backend = PyMarocco.Hardware
    marocco.calib_backend = PyMarocco.XML

    marocco.roqt = "demo.roqt"
    marocco.bio_graph = "demo.dot"

    h276 = pyredman.Hicann()
    #h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(223)))
    marocco.defects.inject(HICANNGlobal(Enum(276)), h276)

    h277 = pyredman.Hicann()
    #h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(2)))
    marocco.defects.inject(HICANNGlobal(Enum(277)), h277)

    marocco.membrane = "membrane.dat"
    marocco.analog_enum = 0
    marocco.hicann_enum = HICANNGlobal(Enum(276)).id().value()

    marocco.pll_freq = 100e6
    marocco.bkg_gen_isi = 10000
    marocco.only_bkg_visible = False


    pynn.setup(marocco=marocco)

else:
    import pyNN.nest as pynn

# helper function for populations
# could (should) be used for spinnaker as well
def get_pops(n_in_pop, hicann, n_used_neuronblocks = 7):

    # neurons needed to fill up buffer
    if simulator_name == "NM-PM1":
        n_in_tmp = 32/(neuron_size/2) - n_in_pop
    else:
        n_in_tmp = 0

    l = []

    for _ in xrange(n_used_neuronblocks):
        pop = pynn.Population(n_in_pop, pynn.IF_cond_exp, params)
        l.append(pop)
        if simulator_name == "NM-PM1":
            marocco.placement.add(pop, HICANNGlobal(Enum(hicann)))

        if n_in_tmp:
            tmp = pynn.Population(n_in_tmp, pynn.IF_cond_exp, params)
            l_tmp.append(tmp)
            if simulator_name == "NM-PM1":
                marocco.placement.add(tmp, HICANNGlobal(Enum(hicann)))

    return l

# from here on it should be plain pynn

duration = 1*30000 #ms

params = {
                'cm'            :   0.2,
                'v_reset'       :  -70,
                'v_rest'        :  -50,
                'v_thresh'      :  -47,
                'e_rev_I'       : -60,
                'e_rev_E'       : -40,
}

if simulator_name == "NM-PM1":
    params['tau_refrac'] = 20
    params['tau_m'] = 409

l_tmp = []

n_in_pop = 12

# prepare populations
# for spinnaker, the hicann number is ignored
pops = []
pops.append(get_pops(n_in_pop, 276))
pops.append(get_pops(n_in_pop, 277))
# -> makes 14 population

# flatten
all_pops = []
for ppops in pops:
    for pop in ppops:
        all_pops.append(pop)

# synaptic weight, must be tuned for spinnaker
w_exc =  0.004

con_alltoall = pynn.AllToAllConnector(weights=w_exc)
con_fixednumberpre = pynn.FixedNumberPreConnector(n=4, weights=w_exc)

# record membrane of one neuron
pynn.PopulationView(all_pops[0], [0]).record_v()

# stimulate the first population with a single spike (3 times)
spike_times = [0, 1000, 2000]
in_0 = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times': spike_times})
for _ in xrange(4):
    for n in xrange(n_in_pop):
        pynn.Projection(in_0, pynn.PopulationView(all_pops[0],[n]), con_alltoall, target='excitatory')

def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

# connect all populations, but don't close the chain
con = con_fixednumberpre
#con = con_alltoall
for pop_a, pop_b in zip(all_pops, shift(all_pops, 1)[:-1]):
    pynn.Projection(pop_a, pop_b, con, target='excitatory')

pynn.run(duration)
pynn.end()

# collect and record spikes
asm = pynn.Assembly()

for pop in all_pops:
    asm += pop

for pop in l_tmp:
    asm += pop

spikes = asm.getSpikes()

print spikes
print "N spikes", len(spikes)

np.savetxt("spikes.dat",spikes)
