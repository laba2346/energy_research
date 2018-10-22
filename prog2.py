from config import *
import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    load, price, pred_price = simulate()
    t = np.arange(0, 96, 1)
    # fig, ax1 = plt.subplots()
    #
    # color = 'tab:red'
    # ax1.set_xlabel('time (15 minute intervals')
    # ax1.set_ylabel('load', color=color)
    # ax1.plot(t, np.asarray(load), color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    #
    # ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    #
    # color = 'tab:blue'
    # ax2.set_ylabel('price', color=color)  # we already handled the x-label with ax1
    # ax2.plot(t, np.asarray(price), color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.show()

    fig, (ax1, ax2) = plt.subplots(1,2)
    color1 = 'tab:red'
    color2 = 'tab:green'
    ax1.set_xlabel('time (15 minute intervals)')
    ax1.set_ylabel('load')
    ax1.plot(t, load, color=color1, label='Actual Load')
    ax1.plot(t, loadData, color=color2, label='Predicted Load')
    ax1.legend(loc="upper left")

    color = 'tab:blue'
    ax2.set_xlabel('time (15 minute intervals')
    ax2.set_ylabel('predicted_price')
    ax2.plot(t, pred_price, color=color)
    plt.show()




# This equation was derived from a sample data set spanning 24 hours, with an
# hour between data points. Adjusted to allow for values of t that represent
# 15 minute intervals.
def calc_pred_load(t):
    #return (2.2/16)*t**2 + (73/4)*t + (1188/4)
    if(t > 0):
        wind = random.randint(-50, 50)
        return loadData[t] + wind
    else:
        return 400

# If higher than the max load, set load to the max load
# If lower than the min load, set load to the min load
# If between min and max, return the load as is
def bound(load, pred_load):
    min = .60*pred_load/5
    max = 1.33*pred_load/5

    if(load < min):
        load = min
    elif(load > max):
        load = max

    return load

def simulate():
    # Keep track of actual price and load of the system over a 24 hour period,
    # in 15 minute intervals.
    act_load = []
    act_price = []
    pred_price_list = []
    for t in range(0, 96):
        pred_load = calc_pred_load(t)
        pred_price = (2*a*pred_load + b)/4000
        # If we are beyond the first time step and have data for act_price,
        # we can calculate the actual load of the system
        if(t > 0):
            total_load = 0
            for j in range(0, 5):
                d = coefficients[j]
                user_load = pred_load/5 + d*(pred_price-.03)
                total_load += bound(user_load, pred_load)
            act_load.append(total_load)
            act_price.append((2*a*total_load + b)/4000)

#actual load, predicted price

        # If we are at the first time step, simply set the load and price to the
        # predicted values
        else:
            act_load.append(pred_load)
            act_price.append(pred_price)

        pred_price_list.append(pred_price)
    return act_load, act_price, pred_price_list

if __name__ == "__main__":
    main()
