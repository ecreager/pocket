import constraint
import string

DEFAULT_N = 4
DEFAULT_FORMAT_FLAG = '0%ib' % DEFAULT_N


def gray_code_bits(n):
    if (not (n % 1.0 == 0.0)) or (n < 1):
        print(n)
        print(not (n % 1.0 == 0.0))
        print(n < 1)
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


def print_possible_shifts(n, format_flag=DEFAULT_FORMAT_FLAG):
    possible_shifts = dict()
    for i in range(2**n):
        possible_shifts[i] = [i ^ (1 << j) for j in range(n)]

    for num, shift in possible_shifts.iteritems():
        formatted_shift = [format(x, format_flag)  for x in shift]
        print('possible shifts for %s: %s' % (format(num, format_flag), formatted_shift))
    return


def valid_neighbors(a, b, format_flag=DEFAULT_FORMAT_FLAG):
    return hamming(a, b, format_flag) == 1


def hamming(a, b, format_flag=DEFAULT_FORMAT_FLAG):
    a_binary, b_binary = format(a, format_flag), format(b, format_flag)
    count = 0
    for aa, bb in zip(list(a_binary), list(b_binary)):
        if aa != bb:
            count += 1
    return count


def solve_1d_gray_code(n=DEFAULT_N, m=None, do_print=True, looping=True):
    """print all length-m codes of n-bit binary numbers such that each adjacent numbers in
    each code share all but one bit in their binary representations, i.e. are valid Gray code transitions"""
    if m is None:
        m = n
    all_keys = get_unique_variables(n)
    format_flag = '0%ib' % m
    problem = constraint.Problem()
    problem.addVariables(all_keys[:2**n], range(2**m))
    problem.addConstraint(constraint.AllDifferentConstraint())
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


def single_1d_gray_code(n=DEFAULT_N, m=None, do_print=True, looping=True):
    """return a single length-n code of m-bit binary numbers such that each adjacent numbers in
    the code share all but one bit in their binary representations, i.e. are valid Gray code transitions"""
    if m is None:
        m = n
    all_keys = get_unique_variables(n)
    format_flag = '0%ib' % m
    problem = constraint.Problem()
    problem.addVariables(all_keys[:2**n], range(2**m))
    problem.addConstraint(constraint.AllDifferentConstraint())
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
    return numeric_soln(soln, all_keys)



def get_unique_variables(n):  # get 2**n unique variable names
    letters = list(string.lowercase)
    n_alphabets = 2**n // len(letters) + 1
    variables = letters
    for i in range(1, n_alphabets):
        variables = letters + [a + b for a, b in zip(letters*i, variables)]
    return variables[:2**n]


def numeric_soln(soln, all_keys):  # convert from symbolic keys to numeric ones
    nsoln = dict()
    for i, key in enumerate(soln.keys()):
        nsoln[i] = soln[all_keys[i]]
    return nsoln


def single_2d_gray_code(n=DEFAULT_N, m=None, do_print=True, looping=True):
    """return a single n-by-n code of m-bit binary numbers such that each adjacent numbers in
    the n-by-n square share all but one bit in their binary representations, i.e. are valid Gray code transitions"""
    if m is None:
        m = n
    format_flag = '0%ib' % m
    problem = constraint.Problem()
    symbols, values = square_variables(n=n, m=m)
    problem.addVariables(symbols.values(), values)
    problem.addConstraint(constraint.AllDifferentConstraint())
    constrs = square_constraints(symbols=symbols, n=n, format_flag=format_flag)
    for constr in constrs:
        problem.addConstraint(*constr)
    soln = problem.getSolution()
    if do_print:
        print('soln')
        for i in range(n):
            for j in range(n):
                key = '(%i, %i)' % (i, j)
                print('%s | %s' % (key, format(soln[key], format_flag)))
    return soln


def square_variables(n, m):
    """dict of symbols and list of values for m-bit binary numbers arranged in an n-by-n square;
    symbols maps array indices to string encoding those indices"""
    symbols = dict()
    values = range(2**m)
    for i in range(n):
        for j in range(n):
            symbols[(i, j)] = '(%i, %i)' % (i, j)
    return symbols, values


def square_constraints(symbols, n=DEFAULT_N, format_flag=DEFAULT_FORMAT_FLAG):
    constrs = []
    neighbor_constraint_fn = lambda a, b: valid_neighbors(a, b, format_flag)
    for i, ii in zip(range(n-1), range(1, n)):
        for j in range(n):
            constrs.append((neighbor_constraint_fn, (symbols[(i, j)], symbols[(ii, j)])))
    for i in range(n):
        for j, jj in zip(range(n-1), range(1, n)):
            constrs.append((neighbor_constraint_fn, (symbols[(i, j)], symbols[(i, jj)])))
    return constrs



