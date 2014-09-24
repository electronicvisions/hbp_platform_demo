class Column(object):

    def __init__(self,params,sim,column_index,logger):

        self.index=column_index

        import pyNN.random as random
        self.Synfire_RNG = random.NumpyRNG(seed=2980123, parallel_safe=True)
        
        self.logger=logger
        self.params=params
        self.logger.info("Creating Column number %d" % column_index)
        self.simulator=sim

        self.create_populations()
        self.connect_populations()
        self.prepare_recording()

    def create_populations(self):

        self.neurons_per_column_INH = int(self.params["neuron_count"] * self.params["INH_proportion"])
        self.neurons_per_column_EXC = self.params["neuron_count"] - self.neurons_per_column_INH

        self.logger.info("Creating %d excitatory cells" % self.neurons_per_column_EXC)
        exec("EXC_celltype = self.simulator.%s" % self.params['neuronmodel'])
        self.EXC_cells=self.simulator.Population(self.neurons_per_column_EXC, EXC_celltype, self.params['neuronparams'][self.params['neuronmodel']])
        self.EXC_cells.initialize('v', self.params['neuronparams'][self.params['neuronmodel']]['v_rest'])


        self.logger.info("Creating %d inhibitory cells" % self.neurons_per_column_INH)
        exec("INH_celltype = self.simulator.%s" % self.params['neuronmodel'])
        self.INH_cells=self.simulator.Population(self.neurons_per_column_INH, INH_celltype, self.params['neuronparams'][self.params['neuronmodel']])
        self.INH_cells.initialize('v', self.params['neuronparams'][self.params['neuronmodel']]['v_rest'])

    def connect_populations(self):

        self.logger.info("Connecting local populations")
        self.logger.info("p = %f" % self.params["local_prob_INH_EXC"])

        EXC_sample_num = int(self.params['local_prob_INH_EXC']*self.neurons_per_column_EXC)
        EXC_incoming_num = int(self.params['local_prob_INH_EXC']*self.neurons_per_column_INH)
        connector_local_INH_EXC = self.simulator.FixedNumberPreConnector(EXC_incoming_num, allow_self_connections=False, weights=self.params['local_weight_INH_EXC'], delays=self.params['local_delay_INH_EXC'])

        if self.params['STP']:
            tso_model_ee=sim.TsodyksMarkramMechanism(U=0.27, tau_rec=400.0, tau_facil=0.0)
            tso_model_ei=sim.TsodyksMarkramMechanism(U=0.27, tau_rec=400.0, tau_facil=0.0)
            tso_model_ie=sim.TsodyksMarkramMechanism(U=0.27, tau_rec=0.0, tau_facil=400.0)
        else:
            tso_model_ee=None
            tso_model_ei=None
            tso_model_ie=None

        syn_dynamics = tso_model_ie
        if self.params['STP']:
            syn_dynamics = self.simulator.SynapseDynamics(fast=tso_model_ie)

        self.proj_rsnp_pyr = self.simulator.Projection(self.INH_cells, self.EXC_cells, connector_local_INH_EXC, target='inhibitory', synapse_dynamics=syn_dynamics, rng=self.Synfire_RNG)
        self.logger.info("local connections INH(%d) to EXC(%d): %d" %
                         (self.index, self.index, len(self.proj_rsnp_pyr)))


    def prepare_recording(self):
        self.EXC_cells.record()
        self.INH_cells.record()
        if self.params['record_voltages']:
            if self.params['EXC_sample_len']:
                self.EXC_cells.sample(self.params['EXC_sample_len']).record_v()
            if self.params['INH_sample_len']:
                self.INH_cells.sample(self.params['INH_sample_len']).record_v()
            #self.simulator.record_v(self.EXC_cells.cell[0], 'mem.dat')     # only for Spikey, which can record only 1 cell at a time

