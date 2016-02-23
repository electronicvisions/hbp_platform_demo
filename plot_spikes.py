import numpy as np
import random
import argparse


def raster(times, neurons, color='k'):
    import matplotlib.pyplot as plt

    ax = plt.gca()

    neurons = np.array(neurons)

    plt.vlines(times, neurons-0.45, neurons + 0.45, color=color, linewidth=1.5)

    plt.xlabel('bio time [s]')
    plt.ylabel('neuron index')

    return ax

def plot(infilename, outfilename="", show=False, xlim=None, ylim=None):
    """
    infilename: first column neuron ids
                second column spike times

    show: [bool] show plot on screen

    outfilename: e.g. result.pdf, result.png

    xlim: (xmin, xmax)

    ylim: (ymin, ymax)
    """
    if not show:
        import matplotlib as mpl
        mpl.use('Agg')

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    ticker.Locator.MAXTICKS *= 100

    spikes = np.loadtxt(infilename)

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

    if xlim:
        plt.xlim(*xlim)

    if ylim:
        plt.ylim(*ylim)
        yticks = np.arange(ylim[0], ylim[1], 10.0)
    else:
        plt.ylim(min(neurons)-0.5, max(neurons)+0.5)
        yticks = np.arange(min(neurons), max(neurons)+1, 10.0)

    plt.yticks(yticks)

    plt.tick_params(axis='x', which='minor', bottom='off', top='off')

    #ax.grid(True)
    #for y in [11.5+12*n for n in xrange(15)]:
    #    plt.axhline(y)

    if outfilename:
        plt.savefig(outfilename)
    if show:
        plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('--plotfilename', default="")
    parser.add_argument('--xlim', type=float, nargs=2, default=None)
    parser.add_argument('--ylim', type=float, nargs=2, default=None)
    args = parser.parse_args()


    plot(args.file.name, args.plotfilename, True, args.xlim, args.ylim)

if __name__ == "__main__":
    main()
