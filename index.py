from random import gauss, seed, shuffle
from math import fabs

from read_mat import read_ellipse_data
from rnn import error_of_diablo, differential_evolution

def split_data_into_train_and_test(data, test_quota=0.6):
	n = len(data)

	nr_of_tests = int(round(test_quota*n))
	nr_of_trials = n - nr_of_tests
	idxs = [i for i in range(n)]
	shuffle(idxs)

	test_data = []
	trial_data = []

	counter = 0
	for i in range(nr_of_tests):
		test_data.append(data[idxs[counter]])
		counter += 1

	for i in range(nr_of_trials):
		trial_data.append(data[idxs[counter]])
		counter += 1

	return (test_data, trial_data)

head_data = read_ellipse_data()
(test_data, trial_data) = split_data_into_train_and_test(head_data)

seed(1)
dims = 5
nodes_per_layer = [3,2,5]
n = 0
prev = dims
prev += 1
for i in range(len(nodes_per_layer)):
	n += prev*nodes_per_layer[i]
	prev = nodes_per_layer[i]

curry_func = lambda x: error_of_diablo(x, nodes_per_layer, test_data)+ 0.1*sum(fabs(val) for val in x)/len(x)
initial_pop = [[gauss(0, 1.0e-4) for _ in range(n)] for _ in range(20)]

w = differential_evolution( curry_func, initial_pop, 2000)

print(error_of_diablo(w, nodes_per_layer, trial_data))