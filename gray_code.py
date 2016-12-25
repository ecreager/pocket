import numpy
from constraint import *
import string
import scipy.spatial

def gray_code_bits(n):
	if (not (n % 1.0 == 0.0)) or (n < 1):
		print(n)
		print((not (n % 1.0 == 0.0)))
		print((n < 1))
		raise Exception('bad input')
	if n == 1:
		return ['0', '1']
	else:
		bits = gray_code_bits(n-1)
		return ['0' + b for b in bits] + ['1' + b for b in reversed(bits)]


def reflected_binary_code(n):
	bits = gray_code_bits(n)
	d = dict()
	for i, j in zip(range(2**n), bits):
		d[i] = j
	return d

def print_possible_shifts(n):
	possible_shifts = dict()
	for i in range(2**n):
		possible_shifts[i] = [i ^ (1 << j) for j in range(n)]

	for num, shift in possible_shifts.iteritems():
		formatted_shift = [format(x, format_flag)  for x in shift]
		print('possible shifts for %s: %s' % (format(num, format_flag), formatted_shift))
	return


def valid_neighbors(a, b, format_flag):
	return (hamming(a, b, format_flag) == 1)


def hamming(a, b, format_flag):
	a_binary, b_binary = format(a, format_flag), format(b, format_flag)
	count = 0
	for aa, bb in zip(list(a_binary), list(b_binary)):
		if aa != bb:
			count += 1
	return count


def solve_1d_gray_code(n, m=None, do_print=True, looping=True):
	if m is None:
		m = n
	all_keys = get_unique_variables(n)
	format_flag = '0%ib' % m
	problem = Problem()
	problem.addVariables(all_keys[:2**n], range(2**m))
	problem.addConstraint(AllDifferentConstraint())
	for i in range(2**n-1):
		problem.addConstraint(lambda a, b: valid_neighbors(a, b, format_flag), (all_keys[i], all_keys[i+1]))
	problem.addConstraint(lambda a: a == 0, (all_keys[0]))
	if looping:  # only one bit switch from last to first code value
		problem.addConstraint(lambda a, b: valid_neighbors(a, b, format_flag), (all_keys[0], all_keys[2**n-1]))
	else:  # go from start to end of range, e.g., 000 --- 111
		problem.addConstraint(lambda a: a == 2**n-1, (all_keys[2**n-1]))
	solns = problem.getSolutions()
	if do_print:
		for j, soln in enumerate(solns):
			print('soln # %i/%i' % (j, len(solns)))
			for i, key in enumerate(soln.keys()):
				print('%i | %s' % (i, format(soln[all_keys[i]], format_flag)))


def single_1d_gray_code(n, m=None, do_print=True, looping=True):
	if m is None:
		m = n
	all_keys = get_unique_variables(n)
	format_flag = '0%ib' % m
	problem = Problem()
	problem.addVariables(all_keys[:2**n], range(2**m))
	problem.addConstraint(AllDifferentConstraint())
	for i in range(2**n-1):
		problem.addConstraint(lambda a, b: valid_neighbors(a, b, format_flag), (all_keys[i], all_keys[i+1]))
	problem.addConstraint(lambda a: a == 0, (all_keys[0]))
	if looping:  # only one bit switch from last to first code value
		problem.addConstraint(lambda a, b: valid_neighbors(a, b, format_flag), (all_keys[0], all_keys[2**n-1]))
	else:  # go from start to end of range, e.g., 000 --- 111
		problem.addConstraint(lambda a: a == 2**n-1, (all_keys[2**n-1]))
	soln = problem.getSolution()
	if do_print:
		print('soln')
		for i, key in enumerate(soln.keys()):
			print('%i | %s' % (i, format(soln[all_keys[i]], format_flag)))
	return soln


def get_unique_variables(n):  # get 2**n unique variable names
	letters = list(string.lowercase)
	count = 0
	n_alphabets = 2**n // len(letters) + 1
	variables = letters
	for i in range(1, n_alphabets):	
		variables = letters + [a + b for a, b in zip(letters*i, variables)]
	return variables[:2**n]
