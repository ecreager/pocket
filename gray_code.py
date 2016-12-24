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


def gray_code(n):
	bits = gray_code_bits(n)
	d = dict()
	for i, j in zip(range(2**n), bits):
		d[i] = j
	return d

