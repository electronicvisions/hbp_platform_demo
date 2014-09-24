import matplotlib
matplotlib.use("Agg")

import pylab
import logging

from NeuroTools import signals
import pickle

logger = logging.getLogger("master")

################################################################################
# +--------------------------------------------------------------------------+ #
# |                  INCM/ALUF Synfire Chain with FFI                        | #
# +--------------------------------------------------------------------------+ #
################################################################################

class Synfire_FFI(object):
    def __init__(self, sim, params):
        # These objects are used throughout the simulation
        import pyNN.random as random
        self.Synfire_RNG=random.NumpyRNG(1234, parallel_safe=True)

        import columns

        self.params=params
        self.simulator = sim

        self.neurons_per_column_INH = int(self.params["neuron_count"] * self.params["INH_proportion"])
        self.neurons_per_column_EXC = self.params["neuron_count"] - self.neurons_per_column_INH


        self.logger=logger
        self.logger.info("******* Scaling Network *******")
        self.scale_network()

        self.simulator.setup(**self.params['simulator_params'])

        self.logger.info("******* Creating Columns *******")
        self.columns=[]
        for i in range(self.params['column_number']):
            self.columns.append(columns.Column(self.params,sim,i,logger))


        self.logger.info("******* Connecting Columns *******")
        if self.params["connect_loop"]:
            num_connects = self.params['column_number']
            self.logger.info("loop connection")
        else:
            num_connects = self.params['column_number'] - 1
            self.logger.info("open connection")

        for i in range(num_connects):
            j = (i + 1) % self.params['column_number']
            EXC_sample_num = int(self.params['feedfw_prob_EXC_EXC'] * self.neurons_per_column_EXC)
            EXC_incoming_num = int(self.params['feedfw_prob_EXC_EXC'] * self.neurons_per_column_EXC)

            connector_EXC_EXC = sim.FixedNumberPreConnector(EXC_incoming_num, allow_self_connections=False, weights=self.params['feedfw_weight_EXC_EXC'],delays=self.params['feedfw_delay_EXC_EXC'])
            prj_pulse_EXC = self.simulator.Projection(self.columns[i].EXC_cells,self.columns[j].EXC_cells,connector_EXC_EXC,rng=self.Synfire_RNG)
            self.logger.info("projections EXC(%d) to EXC(%d): %d" % (i, j, len(prj_pulse_EXC)))

            INH_sample_num = int(self.params['feedfw_prob_EXC_INH'] * self.neurons_per_column_INH)
            INH_incoming_num = int(self.params['feedfw_prob_EXC_INH'] * self.neurons_per_column_EXC)
            connector_EXC_INH = sim.FixedNumberPreConnector(INH_incoming_num, allow_self_connections=False, weights=self.params['feedfw_weight_EXC_INH'],delays=self.params['feedfw_delay_EXC_INH'])
            prj_pulse_INH = self.simulator.Projection(self.columns[i].EXC_cells,self.columns[j].INH_cells,connector_EXC_INH,rng=self.Synfire_RNG)
            self.logger.info("projections EXC(%d) to INH(%d): %d" % (i, j, len(prj_pulse_INH)))

        self.logger.info("******* Configuring Input Pulse *******")
        self.stimulus=self.input_pulse()


    def scale_network(self):
        """
        normalize the connection probabilities: The number of incoming
        synapses per neuron is the same as in a net with 125 neurons with the
        connection probabilities given py the params dictionary.
        """
        factor = 125.0 / self.params["neuron_count"]
        self.params['local_prob_INH_EXC'] *= factor
        self.params['feedfw_prob_EXC_EXC'] *= factor
        self.params['feedfw_prob_EXC_INH'] *= factor
        self.logger.info("scaling connection probabilities by a factor of %f" % factor)
        self.logger.info("INH->EXC: %f" % self.params['local_prob_INH_EXC'])
        self.logger.info("EXC->EXC: %f" % self.params['feedfw_prob_EXC_EXC'])
        self.logger.info("EXC->INH: %f" % self.params['feedfw_prob_EXC_INH'])

    def input_pulse(self):

        spike_times = pylab.zeros((self.neurons_per_column_EXC,self.params['stimulus_spikes_per_pulsepacket'],self.params['stimulus_repetitions']))
        for rep in range(self.params['stimulus_repetitions']):
            spike_tmp = self.Synfire_RNG.rng.normal(loc=self.params['stimulus_onset']+rep*(self.params['stimulus_isi']),scale=self.params['stimulus_sigma'],size=(self.neurons_per_column_EXC,self.params['stimulus_spikes_per_pulsepacket']))
            spike_times[:,:,rep] = spike_tmp

        self.pulsepacket_cells = self.simulator.Population(self.neurons_per_column_EXC, self.simulator.SpikeSourceArray)
        trafod_spike_times = []
        for index,cell_id in enumerate(self.pulsepacket_cells.all_cells):
            spikes = spike_times[index,:,:].flatten()
            spikes.sort()
            if self.params['simulator']=='hardware.stage1':
                self.simulator.set(cell_id,self.simulator.SpikeSourceArray,{'spike_times':spikes})
            else:
                trafod_spike_times.append(spikes)
        if self.params['simulator']!='hardware.stage1':
            self.pulsepacket_cells.tset('spike_times',pylab.array(trafod_spike_times))

        EXC_sample_num = int(self.params['feedfw_prob_EXC_EXC']*self.neurons_per_column_EXC)
        connector_pulse_EXC = self.simulator.FixedNumberPreConnector(EXC_sample_num, allow_self_connections=False, weights=self.params['feedfw_weight_EXC_EXC'],delays=self.params['feedfw_delay_EXC_EXC'])
        prj_pulse_EXC = self.simulator.Projection(self.pulsepacket_cells,self.columns[0].EXC_cells,connector_pulse_EXC,rng=self.Synfire_RNG)
        self.logger.info("excitatory source projections: %d" % len(prj_pulse_EXC))

        INH_sample_num = int(self.params['feedfw_prob_EXC_INH']*self.neurons_per_column_EXC)
        connector_pulse_INH = self.simulator.FixedNumberPreConnector(INH_sample_num, allow_self_connections=False, weights=self.params['feedfw_weight_EXC_INH'],delays=self.params['feedfw_delay_EXC_INH'])
        prj_pulse_INH = self.simulator.Projection(self.pulsepacket_cells,self.columns[0].INH_cells,connector_pulse_INH,rng=self.Synfire_RNG)
        self.logger.info("inhibitory source projections: %d" % len(prj_pulse_INH))


    def save_data(self):

        self.logger.info("----- Getting spikes -----")

        EXC_spklist=[]
        INH_spklist=[]

        for column in self.columns:
            EXC_spikes=column.EXC_cells.getSpikes()
            INH_spikes=column.INH_cells.getSpikes()
            if self.params['simulator']=='hardware.stage1':
                EXC_spikes[:,0]-=column.index*self.neurons_per_column_INH
                INH_spikes[:,0]-=(column.index+1)*self.neurons_per_column_EXC
            else:
                EXC_spikes[:,0]+=column.index*self.neurons_per_column_EXC
                INH_spikes[:,0]+=column.index*self.neurons_per_column_INH
            EXC_spklist+=EXC_spikes.tolist()
            INH_spklist+=INH_spikes.tolist()

            if self.params["record_voltages"]:
                name = str("%s/EXC_voltage.%d.dat" % (self.params["sim_output_dir"], column.index))
                column.EXC_cells.print_v(name, compatible_output = True)
                name = str("%s/INH_voltage.%d.dat" % (self.params["sim_output_dir"], column.index))
                column.INH_cells.print_v(name, compatible_output = True)


        logger.info("----- Generating NeuroTools SpikeLists -----")

        EXC_spklist = signals.SpikeList(EXC_spklist,range(self.neurons_per_column_EXC * self.params['column_number']),t_start=0,t_stop=self.params['sim_duration'])
        INH_spklist = signals.SpikeList(INH_spklist,range(self.neurons_per_column_INH * self.params['column_number']),t_start=0,t_stop=self.params['sim_duration'])
        logger.info("----- Saving the spikes to a file -----")

        EXC_spklist.save(str("%s/EXC_spikes.dat" % self.params['sim_output_dir']))
        INH_spklist.save(str("%s/INH_spikes.dat" % self.params['sim_output_dir']))

        EXC_spklist.raster_plot()
        pylab.savefig('%s/EXC_spikes.png' % self.params['sim_output_dir'], dpi=100)
        pylab.figure()
        INH_spklist.raster_plot()
        pylab.savefig('%s/INH_spikes.png' % self.params['sim_output_dir'], dpi=100)




    def start(self):
        self.logger.info("******* Starting Simulation *******")
        self.simulator.run(self.params['sim_duration'])
        self.logger.info("*** Simulation done ***")
        self.save_data()
        self.simulator.end()
        self.logger.info("******* Simulation Complete *******")


if __name__=='__main__':
    try:
        params = pickle.load(open("params.pkl"))
        print "********** using parameters from params.pkl **********"
    except IOError:
        print "********** loading parameters.py **********"
        exec("from parameters import parameter_space as params")
    #from parameters import parameter_space as params
    exec("import pyNN.%s as sim" % params['simulator'])
    
    import os
       
    #--------- If given take command line parameters ---------------------#
    
    # load the command line parameters for Synfire Chain width and length
    # if none given proceed wit the default values
    try:
        import argparse  
        parser = argparse.ArgumentParser(description='PyNN Simulation of a Synfire Chain with asynchronous Feed-Forward Inhibition')
        parser.add_argument('-l', '--length', action="store", dest="length", type=int, help='Number of Columns')
        parser.add_argument('-w', '--width', action="store", dest="width", type=int, help='Neurons per Column')
        cmdlineparams = parser.parse_args()
        if cmdlineparams.length != None and cmdlineparams.width != None :
	    params['column_number'] = cmdlineparams.length
	    params['neuron_count'] = cmdlineparams.width
    except:
        print "Warning:: Could not import argparse: hence command line parameters have no effect."
	
    #--------- Prepare the output directory ------------------------------#
            
    sim_output_dir = params['sim_output_dir']
    if not os.access(sim_output_dir, os.F_OK):
        os.makedirs(sim_output_dir)
	
    #--------- Configure logging -----------------------------------------#

    logger = logging.getLogger("master")
    logFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: "\
                                 "%(message)s", datefmt="%d %b %Y %H:%M:%S")
    logHandler = logging.FileHandler(filename="%s/master.log" % sim_output_dir,
                                     mode='w')
    logHandler.setFormatter(logFormatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)

    pylogger = logging.getLogger("PyNN")
    pylogHandler = logging.FileHandler(filename="%s/pyNN.log" % sim_output_dir,
                                     mode='w')
    pylogger.addHandler(pylogHandler)
    pylogger.setLevel(logging.DEBUG)

    #--------- Create and start model - -----------------------------------#
    model = Synfire_FFI(sim,params)
    model.start()
