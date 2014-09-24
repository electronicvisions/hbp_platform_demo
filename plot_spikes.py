import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random
import argparse

ticker.Locator.MAXTICKS *= 10

parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('--plotfilename', default="")
parser.add_argument('--xlim', type=float, nargs=2,default=None)
parser.add_argument('--ylim', type=float, nargs=2,default=None)
args = parser.parse_args()

def raster(times, neurons, color='k'):

    ax = plt.gca()

    neurons = np.array(neurons)

    plt.vlines(times, neurons-0.45, neurons + 0.45, color=color, linewidth=1.5)

    plt.xlabel('bio time [s]')
    plt.ylabel('neuron index')

    return ax

def plot(infilename, outfilename="", xlim=None, ylim=None):
    """
    infilename: first column neuron ids
                second column spike times

    outfilename: e.g. result.pdf, result.png

    xlim: (xmin, xmax)

    ylim: (ymin, ymax)
    """

    spikes = np.loadtxt(args.file.name)

    margins={"left":0.11, "right":0.95, "top":0.95, "bottom":0.11}

    fig = plt.figure()

    times, neurons = spikes[:,1], spikes[:,0]

    #mapped_neurons = []
    #neuron_idx_map = {0:0, 16:1, 22:2, 31:3}
    #for n in neurons:
    #    mapped_neurons.append(neuron_idx_map[n])
    #neurons = mapped_neurons

    ax = raster(times, neurons)

    minorLocator   = ticker.MultipleLocator(0.1)
    ax.xaxis.set_minor_locator(minorLocator)

    plt.subplots_adjust(**margins) 

    if args.xlim:
        plt.xlim(*args.xlim)

    if args.ylim:
        plt.ylim(*args.ylim)
        yticks = np.arange(args.ylim[0], args.ylim[1], 10.0)
    else:
        plt.ylim(min(neurons)-0.5, max(neurons)+0.5)
        yticks = np.arange(min(neurons), max(neurons)+1, 10.0)

    plt.yticks(yticks)

    plt.tick_params(axis='x', which='minor', bottom='off', top='off')

    #ax.grid(True)
    #for y in [11.5+12*n for n in xrange(15)]:
    #    plt.axhline(y)

    if args.plotfilename:
        plt.savefig(args.plotfilename)

if __name__ ==  "__main__":

    plot(args.file.name, args.plotfilename, args.xlim, args.ylim)

    plt.show()
