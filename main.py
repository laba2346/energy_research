from config import *
import random
import matplotlib.pyplot as plt
import numpy as np
import operator
from statistics import mean, variance

def main():
    load, price, pred_price, act_price, act_gen, sell_price = simulate()
    t = np.arange(0, day_pts, 1)

    fig = plt.figure()
    fig2 = plt.figure()
    color1 = 'tab:red'
    color2 = 'tab:green'
    color3 = 'tab:blue'
    color4 = 'tab:purple'

    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    ax3 = fig2.add_subplot(1,1,1)

    ax1.set_xlabel('time (5 minute intervals)')
    ax1.set_ylabel('load')
    ax1.plot(t, load, color=color1, label='Actual Load')
    ax1.plot(t, load_data, color=color3, dashes=[6, 2], label='Predicted Load')
    #ax1.plot(t, act_gen, color=color2, label='Generation')
    ax1.legend(loc="upper left")

    color = 'tab:blue'
    ax2.set_xlabel('time (5 minute intervals)')
    ax2.set_ylabel('price')
    ax2.plot(t, act_price, color=color1, label='Actual Cost')
    ax2.plot(t, sell_price, color=color3, dashes=[6, 2], label='sell Price')
    ax2.legend(loc="upper left")

    ax3.set_xlabel('time (5 minute intervals)')
    ax3.set_ylabel('frequency (Hz)')
    ax3.plot(t, 60 + 0.025*np.subtract(load, act_gen), color=color4)
    ax3.legend(loc="upper left")

    fig.tight_layout()
    plt.show()




# This equation was derived from a sample data set spanning 24 hours, with an
# hour between data points. Adjusted to allow for values of t that represent
# 15 minute intervals.
def calc_pred_load(t):
    return load_data[t]


def wind_data(t):
    return wind[t]

def calc_pred_gen(t):
    return load_data[t]+wind[t]

# If higher than the max load, set load to the max load
# If lower than the min load, set load to the min load
# If between min and max, return the load as is
def bound(load, pred_load):
    min = .7*pred_load/NUM_USERS
    max = 1.3*pred_load/NUM_USERS

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
    buy_price_list = []
    sell_price = []


    for t in range(0, day_pts):
        pred_load = act_load[t-1] if t > 0 else calc_pred_load(t)
        desired_load = calc_pred_load(t)
        pred_generation = act_gen[t-1] if t > 0 else calc_pred_gen(t)
        pred_Pfr = max(0,(pred_generation - pred_load - 0.02 * 1187)) + min(0, (pred_generation - pred_load + 0.02 * 1187))
        AP_pred = (2*pred_Pfr*a + b)/4000
        pred_price = (2 * a * pred_load + b) / 4000 + pred_Pfr * AP_pred
        # If we are beyond the first time step and have data for act_price,
        # we can calculate the actual load of the system
        if(t > 0):
            total_load = 0
            for user in user_list:
                # d is the user's sensitivity to price fluctuations, e is
                # price centroid, flag indicates if they are currently responding
                # to price
                d, centroid_list = user.getUserInfo()
                e = centroid_list[int(t/96)]  # get which section of day we're in
                user_pred_load = desired_load/NUM_USERS
                # Pfr = max(0, (total_load - pred_load - wind - 0.02 * 2125)) + min(0, (total_load - pred_load - wind + 0.02 * 2125))

                if(user.is_responding):
                    user.increment()
                    if(user.finishedResponding()):
                        user.reset()

                if(abs(pred_price-e) > 0.75 and not user.is_responding):
                    user.is_responding = True
                    user.saved_load = d*user_pred_load*(pred_price-e)

                flag = abs(pred_price-e) > 0.5
                user_load_t = user_pred_load - user.saved_load - flag*d*user_pred_load*(pred_price-e)/2

                # Save the value at 119 right when the price warrants it, then user
                # load will be this value for the next 2-4 timesteps
                total_load += bound(user_load_t, pred_load)

                # if the predicted price differs from the user's centroid by more
                # than one dollar, the user will adjust his/her load for the
                # next time step.


            # Wind is added here as a disturbance. set to zero to ignore
            wind = wind_data(t)
            #wind = 0
            act_gen.append(pred_load + wind)
            act_load.append(total_load)
            prod_cost = (2*a*(total_load-wind) + b)/4000
            Pfr = max(0, (total_load - pred_load - wind - 0.02 * 2125)) + min(0, (total_load - pred_load-wind + 0.02 * 2125))
            ancillary_price = Pfr*0.10
            sell_price.append(prod_cost+ancillary_price)
            act_price.append((2*a*total_load + b)/4000 + ancillary_price)
        # If we are at the first time step, simply set the load and price to the
        # predicted values
        else:
            act_load.append(pred_load)
            act_price.append(pred_price)
            act_gen.append(pred_load)
            sell_price.append(0.09)

        pred_price_list.append(pred_price)
        act_price_list.append(act_price)

    return act_load, act_price, pred_price_list, act_price, act_gen, sell_price

if __name__ == "__main__":
    main()