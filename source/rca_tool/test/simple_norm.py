import numpy as np

################################################################
#mean of an array 
def mean (a):
	avg = float(sum(a))/float(len(a))
        return avg
################################
#standard deviation of an array
def stdev (a):
        return np.std(a)
################################
#calculate the stadardized value of a variable a knowing the mean and the standard deviation
def standardized (a, mean, stdev):
        return (a-mean)/stdev
################################
#calculate the normalized value (standardized + rescaled between o and 1) 
def normalized (a, mean, stdev, a_max, a_min):
        if not (a < a_max):
                return 1
        if not (a > a_min):
                return 0
	a_standardized = standardized(a, mean, stdev)
	a_max_standardized = standardized(a_max, mean, stdev)
	a_min_standardized = standardized(a_min, mean, stdev)
	return (a_standardized-a_min_standardized)/(a_max_standardized-a_min_standardized)
#calculate a standardized array 
def standardized_a (a):
        a_standardized = []
        for value in a:
                value_standardized = standardized(value, mean(a), stdev(a))
                a_standardized.append(value_standardized)
        return a_standardized
################################
def normalized_a (a):
        a_normalized = []
        for value in a:
                value_normalized = normalized(value, mean(a), stdev(a), max(a), min(a))
                a_normalized.append(value_normalized)
        return a_normalized
#################################################################
a = [2,4,5,45,56,3,23,12,63,43]
print sum(a)
print len(a)
print mean(a)
print stdev(a) 
for value in a: 
	print standardized(value, mean(a), stdev(a))
for value in a: 
	print normalized(value, mean(a), stdev(a), max(a), min(a))
print standardized_a(a)
print normalized_a(a) 
