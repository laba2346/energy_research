import numpy as np
import math
from random import randint
import matplotlib.mlab as mlab
from matplotlib import pyplot
from statistics import mean, variance

class User:
    def __init__(self, d, price_centroid, num_active_steps):
        self.d = d
        self.price_centroid = price_centroid
        self.is_responding = False
        self.num_active_steps = num_active_steps
        self.active_count = 0
        self.saved_load = 0

    def getUserInfo(self):
        return self.d, self.price_centroid

    def finishedResponding(self):
        return self.active_count == self.num_active_steps

    def increment(self):
        self.active_count += 1

    def reset(self):
        self.active_count = 0
        self.is_responding = False
        self.user_saved_load = 0

NUM_USERS = 100

# coefficients for marginal cost
a = 10
b = 73
c = 1

coefficients = [randint(0, 5) for p in range(0, NUM_USERS)]
delays = [randint(1, 5) for p in range(0, NUM_USERS)]

#coefficients = [0, 3, 2, 0, 4]
#centroids = [3, 2.5, 4, 3.5, 2]
load_data = [375.4349172,373.6722292,372.698344,370.9841298,370.1600733,367.9038327,366.5553763,365.3920022,363.7791427,
            362.3469587,361.2452787,359.6720797,357.6317683,355.6619645,353.8463958,353.039966,351.1406698,350.382714,
            349.3779817,348.9064627,348.3644362,348.1132532,347.7430887,347.2451293,347.4566518,346.8441178,346.1566693,
            345.1695642,345.0682097,345.3149858,344.5217763,343.4068762,342.8956967,342.8780698,342.1641812,341.8953712,
            342.7150212,342.7590883,342.6136665,343.2173872,342.7987488,342.9397638,343.7946675,344.2309328,344.4909293,
            344.9404147,344.764146,345.6807437,346.667849,347.7078348,348.7037537,349.5983178,350.5413558,351.797271,
            353.0619997,354.551471,355.9792483,357.7551565,359.9320762,362.6950897,366.0970775,369.0628,371.627511,
            374.4698455,377.9247138,381.7453402,386.1564668,390.2855635,394.40144,399.1871378,403.8979217,409.2256462,
            415.61539,421.2868387,426.2355853,430.5629843,433.8856512,438.0455948,442.2804528,445.9248102,448.4895213,
            451.8386285,454.1565632,457.0429648,461.4232445,465.1865833,467.0638462,468.0685782,468.9719558,469.9810947,
            471.3119242,472.210895,472.3651303,473.6783328,474.1762922,474.9518748,476.6528688,476.7850703,477.4637053,
            477.6664143,476.5647345,474.995942,474.5640835,473.5725715,473.8986688,474.683065,474.9166212,476.0755885,
            477.6003137,478.239288,478.4199635,478.9708035,479.530457,479.199953,479.5436772,478.979617,478.5565718,
            478.5521652,478.2877618,478.6050458,478.8650422,478.9663968,478.3847098,478.0409857,477.2874365,476.6704957,
            476.4721933,475.8905062,475.3484797,474.2203593,473.2949482,473.1186793,473.7929075,473.5285043,473.2729145,
            473.1803735,472.8498695,472.0434397,471.6336147,471.2458233,470.3248188,469.5183892,469.126191,469.0468702,
            469.0733103,469.126191,468.9014483,468.733993,467.94519,467.473671,466.4777523,466.230976,464.8737063,
            465.0015012,463.7588062,463.0140703,463.0140703,462.264928,461.965271,461.8022223,461.3879907,460.5595273,
            459.6120825,459.4446272,458.6161638,458.109391,457.5232973,456.5714458,456.7212742,456.3555165,455.8090832,
            455.1304483,454.3240185,453.0769168,453.1386108,452.6626852,451.6667663,451.2260943,450.3271235,449.564761,
            449.5206938,449.2783242,449.3223913,448.9257865,449.1373092,449.0579882,449.785097,450.0450935,449.9437388,
            450.428478,451.1159263,452.019304,452.6582785,454.16097,455.5226463,457.7304132,459.3256458,461.3307033,
            463.635418,465.4113262,468.403489,472.1580143,476.097622,479.9050282,483.7961618,486.9690003,490.7147123,
            494.134327,497.3380125,500.4667837,504.4152048,508.4826073,512.1974723,516.4455503,520.715662,524.7962848,
            531.2036557,536.7517162,540.7970852,543.3221357,544.1594125,543.458744,544.0580578,543.5116247,543.018072,
            543.5116247,542.0750338,540.673697,538.8360947,536.8883245,534.645304,533.433456,530.8863718,529.2250383,
            528.2511533,525.893558,524.39968,522.9807162,521.535312,519.9400793,518.3933207,516.828935,515.0001462,
            513.1889843,511.589345,509.7341158,507.7775322,505.8033217,503.7586035,501.3481277,499.1579878,496.6858178,
            494.2885622,491.3580935,488.784569,486.3696863,483.2673555,479.6274048,476.4281262,473.2376608,469.8224528,
            465.5259008,462.0886592,457.7083795,453.0945437,449.2606973,445.3827837,441.49165,436.675105,432.5151613,
            428.8487702,425.1515322,421.5644622,417.9994257,414.1435457,409.9880087,404.6602842,400.3945792,397.0102182,
            394.542455,391.5194452,389.3777792,387.2228932,384.9093652,382.55177,380.991791,378.6650428,376.2986342,]

general_pred_price = [(2*a*load + b)/4000 for load in load_data]

day_pts = 288 # number of points in one day (288 = 5 min simulation steps)

mu_one = mean(general_pred_price[:96])
mu_two = mean(general_pred_price[96:192])
mu_three = mean(general_pred_price[192:])

#var_one = variance(general_pred_price[:72])*5
#var_two = variance(general_pred_price[72:208])*5
#var_three = variance(general_pred_price[208:])*5

var_one = 0.5;
var_two = 0.5;
var_three = 0.5;

first_samples = np.random.normal(mu_one, var_one, NUM_USERS)
print("-----PRICE CENTROID FIRST TIER------")
print(mu_one)
print("-----VARIANCE-----")
print(var_one)
second_samples = np.random.normal(mu_two, var_two, NUM_USERS)
print("-----PRICE CENTROID SECOND TIER------")
print(mu_two)
print("-----VARIANCE-----")
print(var_two)
third_samples = np.random.normal(mu_three, var_three, NUM_USERS)
print("-----PRICE CENTROID THIRD TIER------")
print(mu_three)
print("-----VARIANCE-----")
print(var_three)

# plotting distributions
bins = np.linspace(-0.25, 3.25, NUM_USERS)

pyplot.hist(first_samples, bins, alpha=0.5, normed=True, label='morning')

# Empirical average and variance are computed
avg = np.mean(first_samples)
var = np.var(first_samples)
# From that, we know the shape of the fitted Gaussian.
pdf_x = np.linspace(np.min(first_samples),np.max(first_samples),NUM_USERS)
pdf_y = 1.0/np.sqrt(2*np.pi*var)*np.exp(-0.5*(pdf_x-avg)**2/var)
pyplot.plot(pdf_x,pdf_y,'b')

pyplot.hist(second_samples, bins, alpha=0.5, normed=True, label='midday')

# Empirical average and variance are computed
avg = np.mean(second_samples)
var = np.var(second_samples)
# From that, we know the shape of the fitted Gaussian.
pdf_x = np.linspace(np.min(second_samples),np.max(second_samples),NUM_USERS)
pdf_y = 1.0/np.sqrt(2*np.pi*var)*np.exp(-0.5*(pdf_x-avg)**2/var)
pyplot.plot(pdf_x,pdf_y,'tab:orange')

pyplot.hist(third_samples, bins, alpha=0.5, normed=True, label='evening')

# Empirical average and variance are computed
avg = np.mean(third_samples)
var = np.var(third_samples)
# From that, we know the shape of the fitted Gaussian.
pdf_x = np.linspace(np.min(third_samples),np.max(third_samples),NUM_USERS)
pdf_y = 1.0/np.sqrt(2*np.pi*var)*np.exp(-0.5*(pdf_x-avg)**2/var)
pyplot.plot(pdf_x,pdf_y,'g')
pyplot.legend(loc='upper right')
pyplot.show()

user_list = [User(coefficients[i], [first_samples[i], second_samples[i], third_samples[i]], delays[i]) for i in range(NUM_USERS)]
