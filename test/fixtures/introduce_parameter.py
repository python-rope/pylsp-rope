import sys


def main(new_parameter=sys.stdin):
    a = int(new_parameter.read())
    b = 20
    print(a + b)
    c = a + b


a, b = 30, 40
print(a + b)
