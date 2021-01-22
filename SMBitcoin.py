import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys
import numpy as np


# This function retrieves the minima profitability times
# for each simulation we made
def GetWinTime(configs):
    min_times = []
    for config in configs:
        min_times.append(config["min_T"])
    return min_times


# This function computes the average revenue for each
# simulation we are run
def ComputeRevenue(configs):
    reward_S = []
    for elem in configs:
        T = elem["T"]
        reward_S.append(elem["rev_S"] / T)
    return reward_S


# This function is called each time a block is appended
# to the official blockchain. It computes the average revenue
# for the selfish miner from the start up to the time of
# publishing a block
def CheckBestRevenue(config):
    T = config["T"]
    revenue = config["rev_S"] / T
    if (revenue > config["q"]) and T > 2000:
        config["min_T"] = T
        config["rev_flag"] = False


def Compete(config):
    # In this function we simulate a competition between a honest
    # block and a selfish block. The winner is decide by the first
    # miner to mine a new block and this results in three possible
    # cases. In a scenario where Selfish is connected to a fraction gamma
    # of honest miners, the probabilities of winning are:
    # - for S to mine on S block: q
    # - for H to mine on S block: gamma*(1-q)
    # - for H to mine on H block: (1-gamma)*(1-q)

    # competition is won by who mines the next block
    q = config["q"]
    g = config["gamma"]
    added_H_hashpower = g * (1 - q)
    u = rng.random()  # u~U[0,1)
    if (0 < u) and (u <= q):  # Selfish mines on selfish
        config["rev_S"] += 2
        T = 1 / config["alpha_S"]
    elif (q <= u) and (u < q + added_H_hashpower):  # Honest mines on selfish
        config["rev_S"] += 1
        T = 1 / (config["alpha_H"] * g)
    elif q + added_H_hashpower <= u:  # Honest mines on honest
        T = 1 / (config["alpha_H"] * (1 - g))

    config["cyc_T"] += T
    config["T"] += T
    # updating cycle counter by two as two blocks get added, one gets orphaned
    config["cyc_cnt"] += 2
    # zeroing, as now no miner has blocks left
    config["H_n"] = 0
    config["S_n"] = 0

    # checking if difficulty need to be updated
    if config["cyc_cnt"] >= 2016:
        UpdateDifficulty(config)

    if config["rev_flag"]:
        CheckBestRevenue(config)


def SelfishCompetition(config):
    # In this function we simulate the step where a selfish miner
    # having more than 2 blocks publishes one of his blocks each time
    # an honest miner publishes one block. What happens in the long
    # run is that, after the selfish miner S is caught by the honest
    # miners H and he has only 1 block of advantage, he publishes his
    # last two blocks and the blockchain adopts the full selfish fork,
    # rewarding the selfish miner.

    # H's block will get orphaned at the end of the attack, while
    # S's block will get adopted once the blockchain gets rearranged
    config["cyc_cnt"] += 1
    config["rev_S"] += 1

    config["S_n"] += -1  # selfish miners publishes 1 block
    config["H_n"] = 0  # honest miners publishes 1 block (in the end it gets orphaned)

    if config["cyc_cnt"] >= 2016:
        UpdateDifficulty(config)

    if config["rev_flag"]:
        CheckBestRevenue(config)


def PublishSelfish(config):
    # In this function we simulate the step where a selfish miner
    # has only one block of advantage, while the Honest miner has
    # none. Then S publishes his last block, rearranging to whole
    # blockchain to his advantage. Since the function "SelfishCompetition"
    # is written to take into account this last rearranging phase,
    # in this function we just add one block of revenue to the selfish.

    config["cyc_cnt"] += 1
    config["rev_S"] += 1

    config["S_n"] = 0  # selfish miner publishes 1 block

    if config["cyc_cnt"] >= 2016:
        UpdateDifficulty(config)

    if config["rev_flag"]:
        CheckBestRevenue(config)


def PublishHonest(config):
    # This function is called when the honest miner
    # has one block and the selfish has none. It represents
    # the publishing of one block to the official blockchain.
    config["cyc_cnt"] += 1
    config["H_n"] = 0

    if config["cyc_cnt"] >= 2016:
        UpdateDifficulty(config)

    if config["rev_flag"]:
        CheckBestRevenue(config)


def UpdateDifficulty(config):
    # This function is called everytime a block
    # is added to the official blockchain. There is
    # a preemptive check before the function call to
    # avoid overhead time, but if this function is called
    # we update the difficulty counter and the mining
    # speeds by the same updating factor.
    # There is an hardcoded threshold under which the
    # difficulty cannot drop in order to avoid precision
    # issues; if the difficulty drops too low the simulation
    # is gracefully ended.

    if config["d"] > 2e-200:
        adjustment = config["cyc_cnt"] / config["cyc_T"]
        config["d"] = config["d"] * adjustment
        # update the mean times
        config["alpha_S"] /= adjustment
        config["alpha_H"] /= adjustment
    else:
        config["i"] = config["n"]

    # zeroing the cycle values
    config["cyc_cnt"] = 0
    config["cyc_T"] = 0


def MineABlock(config):
    q = config["q"]
    u = rng.random()  # draw r.v from u~U[0,1)

    # add block to miner and its mining time to cycle
    if u <= q:  # S wins
        config["S_n"] += 1  # adding a block to selfish counter
        T = 1 / config["alpha_S"]  # updating total time
    else:  # H wins
        config["H_n"] += 1  # adding a block to the honest counter
        T = 1 / config["alpha_H"]
    config["T"] += T
    config["cyc_T"] += T


def SimulateASelfishMiningStrategy(q, n, gamma):
    config = {
        "q": q,  # hashrate of S (SELFISH) miner
        "gamma": gamma,  # connectivity of S (SELFISH) miner with honest miners
        "n": n,  # number of attack  cycles
        "i": 0,  # this counter is used to prevent the difficulty to be halved too much
        "alpha_S": q,  # mining speed of S (at the start)
        "alpha_H": 1 - q,  # mining speed of H (at the start)
        "d": 1,  # difficulty
        "T": 0,  # total time passed, as sum of time passed per cycle
        "rev_S": 0,  # blocks mined by S during the simulation
        "cyc_T": 0,  # total time passed in a cycle
        "cyc_cnt": 0,  # blocks added in a cycle
        "S_n": 0,  # number of blocks mined by S in an attack attempt
        "H_n": 0,  # number of blocks mined by H in an attack attempt
        "rev_flag": True,
        "min_T": 0,
    }

    # starting the attack
    while config["i"] < config["n"]:
        config["i"] += 1

        # for each attack attempt, reset the starting blocks
        config["S_n"] = 0
        config["H_n"] = 0

        # we mine the first block
        MineABlock(config)

        # 1st phase: if honest miners win, start attack again
        if config["H_n"] == 1:
            PublishHonest(config)
            continue

        # 2nd phase: mine again. Here we have S_n = 1
        elif config["S_n"] == 1:
            MineABlock(config)

            # S_n = H_n = 1. Competition ensues
            if config["H_n"] == 1:
                # Mining a block with parameter gamma to determine who gets the reward!
                Compete(config)
                continue

            # S_n = 2,  H_n = 0. Beginning of selfish mining
            elif config["S_n"] == 2:
                while True:
                    # mine block. If H mines it...
                    MineABlock(config)

                    if config["H_n"] == 1:
                        SelfishCompetition(config)
                    delay = config["S_n"] - config["H_n"]
                    # .. and when H catches S..
                    if delay == 1:
                        PublishSelfish(config)
                        break
    return config


def PlotStatistics(x, rev_S, min_times):
    # create figure and axis
    fig, ax = plt.subplots(1, 2, figsize=(15, 8))
    # _ setting plot ranges
    ax[0].set_xlim([0, 0.5])  # fixed range allows for better visual comparison when plot changes
    ax[0].set_ylim([0, max(rev_S)])
    ax[1].set_xlim([0, 0.5])  # fixed range allows for better visual comparison when plot changes
    ax[1].set_ylim([0, max(min_times)])

    # - labels
    ax[0].set_xlabel(r'Hashrate q (#)')
    ax[0].set_ylabel(r'Revenue (b=1, $\tau$=1)')
    ax[1].set_xlabel(r'Hashrate q (#)')
    ax[1].set_ylabel(r'Profitability times ($\tau$=1)')
    # - title
    ax[0].set_title("Revenue for a selfish mining strategy in Bitcoin")
    ax[1].set_title("Profitability times for a selfish mining strategy in Bitcoin")
    # - grid
    ax[0].grid()
    ax[1].grid()
    # define position of the graph inside the figure:
    # - specify left-bottom corner
    plt.subplots_adjust(left=0.1, bottom=0.25)

    # create figure plot
    # - empirical revenue for a selfish mining strategy
    line_S = ax[0].plot(x, rev_S, lw=2)
    # - revenue for a honest mining strategy
    ax[0].plot(x, x, 'r--', lw=2)
    # - theoretical profitability line
    seuil = (1 - gamma) / (3 - 2 * gamma)
    v_line = ax[0].axvline(x=seuil, c='g', ls=':', lw=2)
    # - profitability times
    line_T = ax[1].plot(x, min_times, lw=2)

    # create sliders
    # - set its background color
    axcolor = 'white'
    # - set bottom-left corner of sliders and width/height
    ax_g = plt.axes([0.15, 0.10, 0.70, 0.03], facecolor=axcolor)
    ax_n = plt.axes([0.15, 0.05, 0.70, 0.03], facecolor=axcolor)
    # - plotting sliders
    s_n = Slider(ax_n, 'n', valmin=1, valmax=150000, valinit=n, valstep=1)
    s_g = Slider(ax_g, 'γ', valmin=0, valmax=1, valinit=gamma, valstep=0.1)

    # defining the event of a slider value change
    def update(val):
        g = s_g.val
        n = s_n.val
        configs = GetSelfishMiningData(q, n, g)
        r_S = ComputeRevenue(configs)
        min_times = GetWinTime(configs)
        line_S[0].set_ydata(r_S)
        line_T[0].set_ydata(min_times)
        ax[0].set_ylim([0, max(r_S)])
        s = (1 - g) / (3 - 2 * g)
        v_line.set_xdata(s)
        ax[1].set_ylim([0, max(min_times)])
        fig.canvas.draw_idle()

    s_n.on_changed(update)
    s_g.on_changed(update)

    plt.show()


def GetSelfishMiningData(q, n, gamma):
    configs = []
    for q_i in q:
        print("Completed {0:2.0f}% of the simulation..".format(q_i * 100 / q[-1]))
        net_cfg = SimulateASelfishMiningStrategy(q_i, n, gamma)
        configs.append(net_cfg)
    return configs


#######################################################################################################################
""" This is the structure of the program. Starting parameters are hard coded but can be changed from the picture 
    widgets. 
"""
if __name__ == "__main__":
    # fix seed for reproducibility
    print("We fix the seed for reproducibility")
    rng = np.random.default_rng(42)

    # define some starting parameters for the plot
    n = 75000  # nb of attack cycles
    gamma = 0.5  # connectivity of the attacker
    q = list(np.arange(0, 0.4, 0.04))
    q += list(np.arange(0.4, 0.49, 1 / 100))
    configs = GetSelfishMiningData(q, n, gamma)
    r_S = ComputeRevenue(configs)
    min_times = GetWinTime(configs)
    PlotStatistics(q, r_S, min_times)
