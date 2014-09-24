import os

parameter_space={
#############################
# MANDATORY NEURODB OPTIONS #
#############################

"simulation_module" : "main",
"sim_filename" : "main.py",
"description" : "Test synfire model",
"analysis_tools_dir" : "",

'sim_output_dir':'output',

'simulator':'nest',

################################


# GLOBAL SIMULATION PARAMETERS #
################################

'sim_duration':300,
'sim_input_dir':'input',

'simulator_params':{
    'debug':False,
    'timestep':0.1,
    'tempFolder':'debug',
    'min_delay':0.1,
    'max_delay':2000.0,
    'assertSilence':True,
    'speedupFactor':4000,
    'useSystemSim':True,
    'ess_params': {
        'perfectSynapseTrafo':True,
        'hardwareSetup':'small', # 4 reticles (2x2)
        },
    'mappingAnalysis':False,
    'logfile' : 'output/logfile.txt',
    'loglevel' : 2,
},


###########################
# NEURON MODEL & PARAMETERS #
###########################

#'neuronmodel':'IF_facets_hardware1',
'neuronmodel':'IF_cond_exp',

'neuronparams':{
    'IF_facets_hardware1':{
        'v_reset' :  -68.0,
        'v_rest' :   -63.0,
        'v_thresh' : -55.0,
        'e_rev_I' :  -80.0,
        'tau_syn_E' :  5.0,
        'tau_syn_I' :  5.0,
        'g_leak' :    10.0},
    'IF_cond_exp':{
        # given in the paper
        'cm'       : 0.290, # nF
        'tau_m'    : 290.0 / 29.0, # pF / nS = ms
        'v_rest'   : -70.0, # mV
        'v_thresh' : -57.0, # mV
        'tau_syn_E': 1.0,   # ms
        'tau_syn_I': 10.0 * 4,  # ms
        'tau_refrac' : 2.0, # ms

        # assumed
        #'v_init'   : -70.0, # mV
        'v_reset'   : -70.0, # mV

        # taken out of referenced paper (E.Muller ...)
        'e_rev_E'  : 0.0,    # mV
        'e_rev_I'  : -75.0,  # mV
        },
    },

##########################
# STIMULUS CONFIGURATION #
##########################

'stimulus_onset':50.,
'stimulus_sigma':.1,
'stimulus_isi':200.,
'stimulus_spikes_per_pulsepacket':1,
'stimulus_repetitions':3,

##################################
# SYNFIRE CHAIN MODEL PARAMETERS #
##################################

'column_number':10,
'neuron_count' : 125,
'INH_proportion' : 0.2, # proportion of inhibitory cells in each column

# connection probabilities (taken from paper)

'local_prob_INH_EXC':1.00,
'feedfw_prob_EXC_EXC':0.60,
'feedfw_prob_EXC_INH':0.60,

# connection weights (taken from paper)
# params used for the FeedForward Network

'local_weight_INH_EXC':0.002 / 4.,  # uS
'feedfw_weight_EXC_EXC':0.001 * 3,  # uS
'feedfw_weight_EXC_INH':0.002 * 3,  # uS (0.0035 in case of EFFECTIVE INHIBTION)

# weights taken from orignal Kremkow script
#'local_weight_INH_EXC':0.0035, # also 0.0045 possible
#'feedfw_weight_EXC_EXC':0.0022,
#'feedfw_weight_EXC_INH':0.0035,

# connect the last column to the first?

'connect_loop' : False,

# delays

'local_delay_INH_EXC':4.,
'feedfw_delay_EXC_EXC':20.,
'feedfw_delay_EXC_INH':20.,

# additional parameters #

'jitter':False, # jitter is normally distributed,
'jitter_sigma':0.001,
'STP':False,

# recording parameters #

'record_INH_spikes':True,       # setting this to False could help with Spikey output buffer overflow

'record_voltages':True,
'EXC_sample_len':2,
'INH_sample_len':2,
}
