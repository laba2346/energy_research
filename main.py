from config import *
import random
import matplotlib.pyplot as plt
import numpy as np
import operator

def main():
    load, price, pred_price, act_price, act_gen = simulate()
    t = np.arange(0, 96, 1)

    fig = plt.figure()
    fig2 = plt.figure()
    color1 = 'tab:red'
    color2 = 'tab:green'
    color3 = 'tab:blue'
    color4 = 'tab:purple'

    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax3 = fig2.add_subplot(1, 1, 1)

    ax1.set_xlabel('time (15 minute intervals)')
    ax1.set_ylabel('load')
    ax1.plot(t, load, color=color1, label='Actual Load')
    ax1.plot(t, loadData, color=color3, label='Predicted Load')
    ax1.plot(t, act_gen, color=color2, label='Generation')
    ax1.legend(loc="upper left")

    color = 'tab:blue'
    ax2.set_xlabel('time (15 minute intervals)')
    ax2.set_ylabel('price')
    #ax2.plot(t, pred_price, color=color)
    ax2.plot(t, act_price, color=color1, label='Actual Price')
    ax2.plot(t, pred_price, color=color3, label='Predicted Price')
    ax2.legend(loc="upper left")

    ax3.set_xlabel('time (15 minute intervals)')
    ax3.set_ylabel('frequency (Hz)')
    ax3.plot(t, 60 - np.subtract(act_gen, load)/1187, color=color4)
    ax3.legend(loc="upper left")

    fig.tight_layout()
    plt.show()

# This equation was derived from a sample data set spanning 24 hours, with an
# hour between data points. Adjusted to allow for values of t that represent
# 15 minute intervals.


def calc_pred_load(t):
    return loadData[t]


def calc_pred_gen(t):
    wind_forcast=random.randint(-10, 10)
    return loadData[t]+wind_forcast


# If higher than the max load, set load to the max load
# If lower than the min load, set load to the min load
# If between min and max, return the load as is
def bound(load, pred_load):
    min = .7*pred_load/5
    max = 1.2*pred_load/5

    if(load < min):
        load = min
    elif(load > max):
        load = max

    return load

def simulate():
    # Keep track of actual price and load of the system over a 24 hour period,
    # in 15 minute intervals.
    act_load = [] # actual load consumed
    act_price = [] # actual price (determined by marginal cost of generation)
    act_gen = [] # actual generation
    pred_price_list = []
    act_price_list = []
    act_gen_list = []

    for t in range(0, 96):
        pred_load = calc_pred_load(t)
        pred_generation = calc_pred_gen(t)
        pred_Pfr = max(0, (pred_generation - pred_load - 0.02 *1187)) + min(0, (pred_generation - pred_load + 0.02*1187))
        pred_price = (2*a*pred_load + b)/4000 + pred_Pfr * 0.010
        # If we are beyond the first time step and have data for act_price,
        # we can calculate the actual load of the system
        if(t > 0):
            total_load = 0
            for j in range(0, 5):
                d = coefficients[j] # price sensitivity per customer
                e = p_coeffs[j]  # price centroid per customer
                user_pred_load = pred_load/5
                user_load = user_pred_load - d*user_pred_load*(pred_price-e)
                total_load += bound(user_load, pred_load)
            # Wind is added here as a disturbance
            wind = random.randint(-50, 50)
            act_gen.append(pred_load + wind)
            act_load.append(total_load)
            prod_cost = (2 * a * (total_load) + b) / 4000
            Pfr = max(0, (total_load - pred_load - wind - 0.02 * 2125)) + min(0, (total_load - pred_load-wind + 0.02 * 2125))
            ancillary_price = Pfr * 0.010
            act_price.append(prod_cost + ancillary_price)

#actual load, predicted price

        # If we are at the first time step, simply set the load and price to the
        # predicted values
        else:
            act_load.append(pred_load)
            act_price.append(pred_price)
            act_gen.append(pred_load)

        pred_price_list.append(pred_price)
        act_price_list.append(act_price)
    return act_load, act_price, pred_price_list, act_price, act_gen

if __name__ == "__main__":
    main()