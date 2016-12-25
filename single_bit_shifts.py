import numpy

def print_bit_shifts(n):
	n = 9
	format_flag = '0%ib' % n

	for i in range(2**n):
		print('%i : %s' % (i, format(i, format_flag)))
		for j in range(n):
			print 'shift %i : %s' % (j, format(i ^ (1 << j), format_flag))

def adjacent(x, y, n):
	possible_shifts = [x ^ (1 << j) for j in range(2**n)]
	for shift in possible_shifts:
		if shift == y:
			return True
	return False


def adjacency_matrix(n):
	Z = numpy.zeros((2**n, 2**n))
	for i in range(2**n):
		for j in range(2**n):
			if adjacent(i, j, n):
				Z[i, j] = 1
	return Z


def cost_matrix(n):
	return 1 - adjacency_matrix(n)