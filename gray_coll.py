import gray_code
import os


def write_gray_coll(n=4, m=4):
    """make 2d lookup table of m-bit binary numbers arranged according to Gray code in n-by-n square
    then write it to disk in a Max/MSP-friendly way"""
    code = gray_code.single_2d_gray_code(n=n, m=m, do_print=True)
    string = ''
    for i in range(n):
        string += '%i, ' % (i+1)
        for j in range(n):
            string += '%i ' % code['(%i, %i)' % (i, j)]
        string += ';\n'

    filename = '2d_table.txt'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        f.write(string)
    print('wrote table to disk')

if __name__ == '__main__':
    write_gray_coll()
