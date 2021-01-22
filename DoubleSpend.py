import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np


def ComputeRevenue(H_blocks, S_blocks):
    S_win = sum(i["b"] for i in S_blocks if i["w"])
    S_time = sum(i["t"] for i in S_blocks) + 0.00001
    return S_win / S_time


def GetSatoshiData(n, z, A, k):
    N = 100
    q = []
    r = []
    for i in range(1, N-1, 1):
        q_i = i / (N * 2)
        q.append(q_i)
        H_info, S_info = SimulateASatoshiAttack(n, q_i, z, A, k)
        r_i = ComputeRevenue(H_info, S_info)
        r.append(r_i)
    return q, r


def MineBlock(H_blk, S_blk, q):
    u = rng.random()  # u~U[0,1)
    if u <= q:
        S_blk += 1
    else:
        H_blk += 1
    return H_blk, S_blk

def EnoughConfirmations(H_blk, z):
    return (H_blk >= z)


# "The mathematics of bitcoin", p. 7
def LaggingBehind(H_blk, S_blk, A_max_lag):
    delay = H_blk - S_blk
    return (delay >= A_max_lag + 1)

def SimulateASatoshiAttack(n, q, z, A, k):
    # in this dataframe we store the info about the selfish (S)
    # and honest (H) miners for each cycle

    S_info = []
    H_info = []
    for i in range(n):
        S_blk = k  # at the start of the attack, S has already mined k blocks
        H_blk = 0
        # as soon as honest miner has mined a number of blocks
        # equal to number of confirmations or selfish miner has
        # fallen behind more than what's acceptable, go to the
        # next step
        while not EnoughConfirmations(H_blk, z) and not LaggingBehind(H_blk, S_blk, A):
            # draw random number to simulate Markov Process
            H_blk, S_blk = MineBlock(H_blk, S_blk, q)

        # now there are two possibilities:
        #    - S_miner was lagging behind and gave up > try again attack
        #    - H_miner got enough confirms            > the miner keeps attacking until he either succeeds or gives up
        # we enter this cycle only if (S) is not lagging behind
        # print("Enter second phase")
        while not LaggingBehind(H_blk, S_blk, A):
            # immediately stop cycle if win condition is satisfied
            if S_blk > H_blk:
                break
            H_blk, S_blk = MineBlock(H_blk, S_blk, q)
        # store data
        t_S = S_blk / q
        t_H = H_blk / (1 - q)
        S_info.append({"b": S_blk, "w": (S_blk > H_blk), "t": t_S})
        H_info.append({"b": H_blk, "w": (S_blk < H_blk), "t": t_H})
    return H_info, S_info


if __name__ == "__main__":
    # fix seed for reproducibility
    print("We fix the seed for reproducibility")
    rng = np.random.default_rng(42)
    # create figure and axis
    fig, ax = plt.subplots(figsize=(8,8))
    # adding
    # - labels
    ax.set_xlabel(r'Hashrate q (#)')
    ax.set_ylabel(r'Revenue')
    # - title
    ax.set_title("Revenue for a double spend attack")
    # - axis range
    ax.set_xlim([0, 0.5])  # fixed range allows for better visual comparison when plot changes
    ax.set_ylim([0, 0.6])
    # - grid
    ax.grid()
    # define position of the graph inside the figure:
    # - specify left-bottom corner
    plt.subplots_adjust(left=0.1, bottom=0.35)

    # define some starting parameters for the plot
    n = 100  # nb of attack cycles
    z = 6  # nb of confirmations
    A = 1  # max accepted delay
    k = 1  # (S) premined blocks
    # get X and Y data
    q, r = GetSatoshiData(n, z, A, k)

    # create figure plot
    # - expected revenue for a honest miner
    plt.plot(q, q, 'r--')
    # - empirical revenue for a Satoshi Attack
    l = plt.plot(q, r, lw=2)

    # create sliders
    # - set its background color
    axcolor = 'white'
    # - set bottom-left corner of sliders and width/height
    ax_k = plt.axes([0.15, 0.20, 0.70, 0.03], facecolor=axcolor)
    ax_A = plt.axes([0.15, 0.15, 0.70, 0.03], facecolor=axcolor)
    ax_z = plt.axes([0.15, 0.10, 0.70, 0.03], facecolor=axcolor)
    ax_n = plt.axes([0.15, 0.05, 0.70, 0.03], facecolor=axcolor)
    # - plotting sliders
    s_n = Slider(ax_n, 'n', valmin=1, valmax=1000, valinit=n, valstep=1)
    s_z = Slider(ax_z, 'z', valmin=0, valmax=10, valinit=z, valstep=1, dragging=True)
    s_A = Slider(ax_A, 'A', valmin=1, valmax=6, valinit=A, valstep=1, dragging=True)
    s_k = Slider(ax_k, 'k', valmin=0, valmax=10, valinit=k, valstep=1, dragging=True)

    # defining the event of a slider value change
    def update(val):
        z = s_z.val
        n = s_n.val
        A = s_A.val
        k = s_k.val
        h, r = GetSatoshiData(n, z, A, k)
        l[0].set_ydata(r)
        fig.canvas.draw_idle()


    s_n.on_changed(update)
    s_z.on_changed(update)
    s_A.on_changed(update)
    s_k.on_changed(update)

    plt.show()
