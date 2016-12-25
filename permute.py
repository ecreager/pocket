import numpy

A = numpy.arange(9).reshape((3, 3))
P = numpy.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])

B = A.dot(P)

print('A')
print(A)
print('column-shifted A')
print(B)