import gray_code
import os


def write_gray_table():
    """write a Gray code max msp table"""
    filename = 'gray_table.txt'
    string = 'table '
    n = 7
    m = 7
    code = gray_code.single_1d_gray_code(n=n, m=m, do_print=True)
    for value in code.values():
        string += '%i ' % value
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "w") as f:
        f.write(string)
    print('wrote table to disk')

if __name__ == '__main__':
    write_gray_table()
