from config import *

def main():
    load, price = simulate()
    for item in load:
        print(item)

# This equation was derived from a sample data set spanning 24 hours, with an
# hour between data points. Adjusted to allow for values of t that represent
# 15 minute intervals.
def calc_pred_load(t):
    return (2.2/16)*t**2 + (73/4)*t + (1188/4)

def simulate():
    # Keep track of actual price and load of the system over a 24 hour period,
    # in 15 minute intervals.
    act_load = []
    act_price = []
    for t in range(0, 96):
        pred_load = calc_pred_load(t)
        pred_price = (2.2)*a*pred_load + b

        # If we are beyond the first time step and have data for act_price,
        # we can calculate the actual load of the system
        if(t > 0):
            total_load = pred_load
            for j in range(0, 5):
                d = coefficients[j]
                total_load += d*(act_price[t-1] - pred_price)
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
