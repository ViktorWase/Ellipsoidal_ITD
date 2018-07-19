from math import tanh, sqrt, exp, fabs
from random import random, sample, randint, seed, gauss, shuffle
from copy import deepcopy


import scipy.misc
import matplotlib.pyplot



def squash(x):
	if x < -100.0 or x > 100:
		if x<0:
			return 0.0
		else:
			return 1.0
	return 1.0/(1.0 + exp(-x))
	#return tanh(x)


def diablo_network(weights, Xin, nodes_per_layer):
	assert nodes_per_layer[-1] == len(Xin)
	layers = len( nodes_per_layer )
	dims = len(Xin)

	X = list(Xin)
	X.append(1.0)
	dims += 1
	middle_layer = [0.0] * nodes_per_layer[0]

	counter = 0

	# First layer
	for i in range(nodes_per_layer[0]):
		for j in range(dims):
			middle_layer[i] += weights[counter]*X[j]
			counter += 1
		#middle_layer[i] += weights[counter]
		#counter += 1
		middle_layer[i] = squash(middle_layer[i])

	# Aaaaall the middle ones
	prev_layer = list(middle_layer)
	for layer_nr in range( layers - 1 ):
		middle_layer = [0.0] * nodes_per_layer[layer_nr+1]
		for i in range(nodes_per_layer[layer_nr+1]):
			for j in range(nodes_per_layer[layer_nr]):
				middle_layer[i] += weights[counter]*prev_layer[j]
				counter += 1
			#middle_layer[i] += weights[counter]
			#counter += 1
			if layer_nr != layers - 1 - 1: # We don't squash the last layer
				middle_layer[i] = squash(middle_layer[i])
		prev_layer = list( middle_layer )

	return middle_layer

def error_of_diablo(weights, nodes_per_layer, training_data):
	err = 0.0
	n = len(training_data)

	for i in range(n):
		pic = training_data[i]
		new_pic = diablo_network(weights, pic, nodes_per_layer)

		assert len(pic) == len(new_pic)

		diff = 0.0
		for j in range(len(pic)):
			diff += (pic[j]-new_pic[j]) * (pic[j]-new_pic[j])
		#diff = sqrt( diff )

		err += sqrt(diff)

	return diff/(n*len(pic))


def differential_evolution( func, initial_population, max_iter):
	pop_size = len(initial_population)
	dims = len(initial_population[0])

	parameters = [[random(), random()*0.9+0.1] for _ in range(pop_size)] # cr, f

	fitness_list = [0.0] * pop_size
	for i in range(pop_size):
		fitness_list[i] =  func(initial_population[i])

	best_yet = min( fitness_list )
	print("Best yet:", best_yet)

	#population = deepcopy( initial_population )
	population =  initial_population 
	for itr in range(max_iter):
		if itr%5 == 0 and itr!=0:
			print("Iteration:", itr)
		for p in range(pop_size):
			cr = parameters[p][0]
			f = parameters[p][1]

			if random() < 0.1:
				cr = random()
			if random() < 0.1:
				f = random()*0.9 + 0.1

			three_chosen = sample(range(pop_size-1), 3)
			for i in range(3):
				if three_chosen[i] >= p:
					three_chosen[i] += 1
			new_ind = list( population[p] )
			rid = randint(0, dims)
			for i in range( dims ):
				r = random()
				if r < cr or i == rid:
					new_ind[i] = population[three_chosen[0]][i] + f * (population[three_chosen[1]][i] - population[three_chosen[2]][i])
			new_fitness = func(new_ind)

			if new_fitness < fitness_list[p]:
				fitness_list[p] = new_fitness
				population[p] = list( new_ind )

				parameters[p][0] = cr
				parameters[p][1] = f
				#print("Mean:", sum(f for f in fitness_list)/pop_size, "best yet:", min(fitness_list), best_yet)

				assert pop_size == len(fitness_list)

				if new_fitness < best_yet:
					print("Best yet:", new_fitness, itr)
					best_yet = new_fitness

			if new_fitness < fitness_list[p]:
				fitness_list[index_of_best] = new_fitness
				population[index_of_best] = list( new_ind )

				if new_fitness < best_yet:
					save_one_flag(diablo_network(new_ind, DATA[0], nodes_per_layer ), itr=itr)
					print("Best yet (from es):", new_fitness, itr)
					best_yet = new_fitness

		best_yet = min(fitness_list)
		index_of_best = fitness_list.index(best_yet)

		# Do some small changes to the best ind
		for _ in range(4):
			new_ind = list(population[index_of_best])
			for i in range(len(new_ind)):
				new_ind[i] += gauss(0, 1.0e-5)
			new_fitness = func(new_ind)

	index_of_best = fitness_list.index(best_yet)
	return population[index_of_best]
if __name__ == '__main__':
	seed(1)
	dims = 5
	nodes_per_layer = [5,3,2,3,5]
	n = 0
	prev = dims
	prev += 1
	for i in range(len(nodes_per_layer)):
		n += prev*nodes_per_layer[i]
		prev = nodes_per_layer[i]

	# Add the biases
	#n += sum(nodes_per_layer)

	print("N:", n)

	data = [ [0,1,2,3,4], [1,2,3,4,5], [2,3,4,5,6] ]

	curry_func = lambda x: error_of_diablo(x, nodes_per_layer, data)

	initial_pop = [[gauss(0, 1.0e-4) for _ in range(n)] for _ in range(20)]
	#initial_pop[0] = [0.0 for _ in range(n)]


	w = initial_pop[0]


	w = differential_evolution( curry_func, initial_pop, 1000)
	print("Done")
	print(w)