import matplotlib.pyplot as plt

from deap.tools.support import Logbook

def graph_min_vs_avg(logbook: Logbook, save: bool = False, show: bool = True, \
        name: str = ""):
    """Generates a graph of the minimum and average fitness per generation.

    Args:
        logbook (Logbook): Object containing the relevant data
        save (bool, optional): Save as a png if true. Defaults to False.
        show (bool, optional): Shows the graph if true. Defaults to True.
        name (str, optional): Name for the png file. Defaults to True.
    """    
    gen = logbook.select("gen")
    fit_mins = logbook.select("best")
    fit_avgs = logbook.select("avg")

    fig, ax1 = plt.subplots()
    plt.title("Minimum Fitness vs Average Fitness")
    line1 = ax1.plot(gen, fit_mins, "b-", label="Minimum Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, fit_avgs, "r-", label="Average Fitness")
    ax2.set_ylabel("Fitness", color="r")
    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")

    if save:
        if not name:
            print("Error: need a name to save the file.")
        else:
            plt.savefig('minvsavg_%s.png' % (name))
    if show:
        plt.show()

def graph_val_vs_inv(logbook: Logbook, save: bool = False, show: bool = True, \
        name: str = ""):
    """Generates a graph of the # of valid and invalid 
    individuals per generation.

    Args:
        logbook (Logbook): Object containing the relevant data
        save (bool, optional): Save as a png if true. Defaults to False.
        show (bool, optional): Shows the graph if true. Defaults to True.
        name (str, optional): Name for the png file. Defaults to True.
    """   
    gen = logbook.select("gen")
    invalid, valid = logbook.select("invalid"), logbook.select("valid")

    fig, ax1 = plt.subplots()
    plt.title("Valid Individuals vs Invalid Individuals")
    line1 = ax1.plot(gen, valid, "b-", label="# of Valid individuals")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("# of Valid", color="b")
    for tl in ax1.get_yticklabels():
        tl.set_color("b")

    ax2 = ax1.twinx()
    line2 = ax2.plot(gen, invalid, "r-", label="# of Invalid individuals")
    ax2.set_ylabel("# of Invalid", color="r")
    for tl in ax2.get_yticklabels():
        tl.set_color("r")

    lns = line1 + line2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc="center right")

    if save:
        if not name:
            print("Error: need a name to save the file.")
        else:
            plt.savefig('validvsinvalid_%s.png' % (name))
    if show:
        plt.show()
        