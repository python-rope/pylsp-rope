import sys


def main():
    a = int(sys.stdin.read())
    b = 20
    extracted_method(a, b)
    c = a + b

def extracted_method(a, b):
    print(a + b)


a, b = 30, 40
extracted_method(a, b)
