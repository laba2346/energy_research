from config import *
import random
import matplotlib.pyplot as plt

def main():
    load, price = simulate()
    modifiedLoad = [load+random.randint(0,50) for load in loadData]
    plt.plot(loadData)
    plt.plot(modifiedLoad)
    plt.xlabel("time")
    plt.ylabel("load")
    plt.show()


# This equation was derived from a sample data set spanning 24 hours, with an
# hour between data points. Adjusted to allow for values of t that represent
# 15 minute intervals.
def calc_pred_load(t, act_load):
    #return (2.2/16)*t**2 + (73/4)*t + (1188/4)
    if(t > 0):
        wind = random.randint(0 , 100)
        return act_load[t-1] + wind
    else:
        return 500

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
    for t in range(0, 96):
        pred_load = calc_pred_load(t, act_load)
        pred_price = (2.2)*a*pred_load + b
        # If we are beyond the first time step and have data for act_price,
        # we can calculate the actual load of the system
        if(t > 0):
            total_load = 0
            for j in range(0, 5):
                d = coefficients[j]
                user_load = d*(act_price[t-1] - pred_price) + pred_load/5
                total_load += bound(user_load, pred_load)
            act_load.append(total_load)
            act_price.append((2.2)*a*total_load + b)

        # If we are at the first time step, simply set the load and price to the
        # predicted values
        else:
            act_load.append(pred_load)
            act_price.append(pred_price)

    return act_load, act_price

if __name__ == "__main__":
    main()
