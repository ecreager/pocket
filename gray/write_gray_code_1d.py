import gray_code
import os


def write_gray_code_1d(n=7, m=7, filename='gray_lookup_1d.txt'):
    """write a 1-D Gray code to disk in a Max/MSP-friendly way"""
    string = 'table '
    code = gray_code.single_1d_gray_code(n=n, m=m, do_print=True)
    for value in code.values():
        string += '%i ' % value 
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        f.write(string)
    print('wrote table to disk')


if __name__ == '__main__':
    write_gray_code_1d()
