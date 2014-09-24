# trying to figure out what goes on here...
# ... to make this work on the ESS

import pylogging

import pyhmf as pynn
import numpy as np
import os, sys
from pymarocco import PyMarocco
from pyhalbe.Coordinate import SynapseDriverOnHICANN, HICANNGlobal, X, Y, Enum,  NeuronOnHICANN

import Coordinate as C

import pyhalbe
#pyhalbe.Debug.change_loglevel(0)
pylogging.set_loglevel(pylogging.get("marocco"), pylogging.LogLevel.DEBUG)
pylogging.set_loglevel(pylogging.get("sthal"), pylogging.LogLevel.INFO)
pylogging.set_loglevel(pylogging.get("sthal.HICANNConfigurator.Time"), pylogging.LogLevel.DEBUG)
pylogging.set_loglevel(pylogging.get("Default"), pylogging.LogLevel.INFO)

spike_log = pylogging.get("ESS")
layout = pylogging.ColorLayout(False)
appender = pylogging.FileAppender(layout, "ESS.log", False)
spike_log.addAppender(appender)
spike_log.setAdditivity(False)
pylogging.set_loglevel(spike_log, pylogging.LogLevel.TRACE)

config_log = pylogging.get("hal2ess")
appender = pylogging.FileAppender(layout, "hal2ess.log", False)
config_log.addAppender(appender)
config_log.setAdditivity(False)
pylogging.set_loglevel(config_log, pylogging.LogLevel.TRACE)

calib_log = pylogging.get("Calibtic")
appender = pylogging.FileAppender(layout, "Calibtic.log", False)
calib_log.addAppender(appender)
calib_log.setAdditivity(False)
pylogging.set_loglevel(calib_log, pylogging.LogLevel.TRACE)

#pylogging.default_config(date_format='absolute')

import operator

import pyredman
h = pyredman.Hicann()

import pyredman

# what about this backend
def initBackend(fname):

    lib = pyredman.loadLibrary(fname)

    backend = pyredman.loadBackend(lib)

    if not backend:

        raise Exception('unable to load %s' % fname)

    return backend

#backend = initBackend('libredman_xml.so')
#backend.config('path', '.')
#backend.init()

#use=HICANNGlobal(Enum(276))
#h = pyredman.HicannWithBackend(backend, use)

neuron_size = 4

marocco = PyMarocco()
marocco.placement.setDefaultNeuronSize(neuron_size)
marocco.placement.use_output_buffer7_for_dnc_input_and_bg_hack = True
marocco.placement.minSPL1 = False
# obviously we need ESS backend here
marocco.backend = PyMarocco.ESS
# which calibtic backend??
marocco.calib_backend = PyMarocco.XML

marocco.bio_graph = "foo.dot"

#marocco.routing.syndriver_chain_length = 1

marocco.roqt = "foo.roqt"

# i have no idea about redman...
h276 = pyredman.Hicann()
# this seems to disable loads of syndrivers, which is in principle not necessary on the ESS
# but we want to do the same thing as on HW, so i guess this should stay
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(6)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(10)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(12)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(17)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(28)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(40)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(44)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(50)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(54)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(58)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(62)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(70)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(71)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(79)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(80)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(88)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(89)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(90)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(96)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(102)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(107)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(110)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(111)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(117)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(127)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(133)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(135)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(137)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(141)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(143)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(149)))

h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(159)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(165)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(173)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(181)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(183)))

h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(185)))

h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(189)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(197)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(209)))
h276.drivers().disable(SynapseDriverOnHICANN(C.Enum(223)))
marocco.defects.inject(HICANNGlobal(Enum(276)), h276)



h277 = pyredman.Hicann()
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(2)))
#h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(6)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(12)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(27)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(30)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(34)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(36)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(50)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(54)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(56)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(76)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(82)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(92))) # 20140903
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(100)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(102)))  # 20140903
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(141)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(147)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(155)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(156)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(159)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(163)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(173)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(177)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(189)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(191)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(204)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(206)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(209)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(213)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(215)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(217)))
h277.drivers().disable(SynapseDriverOnHICANN(C.Enum(221)))
marocco.defects.inject(HICANNGlobal(Enum(277)), h277)

# what about this stuff??

"""

h305 = pyredman.Hicann()
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(4)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(6)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(8)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(10)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(16)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(18)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(20)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(26)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(36)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(42)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(44)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(48)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(52)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(54)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(60)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(64)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(66)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(68)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(79)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(82)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(88)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(94)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(98)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(104)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(110)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(113)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(115)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(117)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(122)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(123)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(127)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(129)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(132)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(139)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(141)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(145)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(149)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(155)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(159)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(161)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(163)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(165)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(167)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(171)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(175)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(177)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(179)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(181)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(183)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(185)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(186)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(187)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(191)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(193)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(195)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(197)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(205)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(211)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(212)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(213)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(215)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(217)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(219)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(221)))
h305.drivers().disable(SynapseDriverOnHICANN(C.Enum(223)))
marocco.defects.inject(HICANNGlobal(Enum(305)), h305)
"""

marocco.membrane = "membrane.dat"
marocco.analog_enum = 0
marocco.hicann_enum = HICANNGlobal(Enum(276)).id().value()

marocco.only_bkg_visible = False

marocco.wafer_cfg = "wafer.xml"

#marocco.bkg_gen_isi = 2500
#marocco.bkg_gen_isi = 250
#marocco.bkg_gen_isi = 1250
marocco.pll_freq = 100e6
#marocco.bkg_gen_isi = int(1*marocco.pll_freq/1e4)
marocco.bkg_gen_isi = 10000
#marocco.hicann_configurator = PyMarocco.DontProgramFloatingGatesHICANNConfigurator
#marocco.hicann_configurator = PyMarocco.DontProgramFloatingGatesNorSynapsesHICANNConfigurator

pynn.setup(marocco=marocco)

duration = 3000 #ms
#numInh = 0


inputParameters = {
        'rate'      : 100.0,             # Hz
        'start'     : int(duration*1/4.),     # ms
        'duration'  : int(duration*3/4.)      # ms
}

params = {
                'cm'            :   0.2,
                'tau_m'         :  409.0, # this is I_gl DAC!
                #tau_m'         :  50,
                'v_reset'       :  -70,
                'v_rest'        :  -50,
                'v_thresh'      :  -47,
                #'v_thresh'      :  0,
                'e_rev_I'       : -60,
                'e_rev_E'       : -40,
                'tau_refrac'    : 20 # this is I_pl DAC!
                #'tau_refrac'    : 100
}

l_tmp = []

# what does it do???
def pops_one_hicann(n_in_pop, hicann, n_used_neuronblocks = 7):

    # neurons needed to fill up buffer
    n_in_tmp = 32/(neuron_size/2) - n_in_pop
    #n_in_tmp = 0

    l = []

    for _ in xrange(n_used_neuronblocks):
        pop = pynn.Population(n_in_pop, pynn.IF_cond_exp, params)
        l.append(pop)
        marocco.placement.add(pop, HICANNGlobal(Enum(hicann)))

        if n_in_tmp:
            tmp = pynn.Population(n_in_tmp, pynn.IF_cond_exp, params)
            l_tmp.append(tmp)
            marocco.placement.add(tmp, HICANNGlobal(Enum(hicann)))

    return l

# neurons in population
n_in_pop = 12

pops_hicanns = []

# vertical setup
#pops_hicanns.append(pops_one_hicann(n_in_pop, 280))

pops_hicanns.append(pops_one_hicann(n_in_pop, 276))
#pops_hicanns.append(pops_one_hicann(n_in_pop, 277, 7))
#pops_hicanns.append(pops_one_hicann(n_in_pop, 305))
#pops_hicanns.append(pops_one_hicann(n_in_pop, 304))



spike_times = [1]#, 1000, 2000]
in_0 = pynn.Population(1, pynn.SpikeSourceArray, {'spike_times': spike_times})

w_exc =  0.004
w_inh =  0.0005

con_alltoall = pynn.AllToAllConnector(weights=w_exc)
con_alltoall_weak = pynn.AllToAllConnector(weights=w_inh)
con_onetoone = pynn.OneToOneConnector(weights=w_exc)
con_fixednumberpre = pynn.FixedNumberPreConnector(n=4, weights=w_exc)
con_fixednumberpre_weak = pynn.FixedNumberPreConnector(n=4, weights=w_inh)

con = con_fixednumberpre
#con = con_alltoall

all_pops = []

for hicann_pops in pops_hicanns:
    for pop in hicann_pops:
        all_pops.append(pop)

pynn.PopulationView(all_pops[0], [0]).record_v()

# give spike input to the first neurons
for _ in xrange(4):

    for n in xrange(n_in_pop):
        pynn.Projection(in_0, pynn.PopulationView(all_pops[0],[n]), con_alltoall, target='excitatory')

def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

for pop_a, pop_b, pop_c, pop_d in zip(all_pops, shift(all_pops, 1)[:-1], shift(all_pops, 2), shift(all_pops,3)):
#for pop_a, pop_b, pop_c, pop_d in zip(all_pops, shift(all_pops, 1), shift(all_pops, 2), shift(all_pops,3)):

    pynn.Projection(pop_a, pop_b, con, target='excitatory')
    #pynn.Projection(pop_b, pop_a, con_alltoall_weak, target='inhibitory')

pynn.run(duration) # ms

try:
    pynn.end()
except RuntimeError as e:
    print e

asm = pynn.Assembly()

for hicann_pops in pops_hicanns:
    for pop in hicann_pops:
        asm += pop

for pop in l_tmp:
    asm += pop


#asm += pop_hicann_277
#asm += pop_hicann_305
#asm += pop_hicann_304
#
#asm += pop_hicann_276_2
#asm += pop_hicann_277_2
#asm += pop_hicann_305_2
#asm += pop_hicann_304_2

#
##dummy
#asm += pop_hicann_278
#asm += pop_hicann_279
#asm += pop_hicann_306
#asm += pop_hicann_307

spikes = asm.getSpikes()

print spikes
print "N spikes", len(spikes)

np.savetxt("spikes.dat",spikes)

