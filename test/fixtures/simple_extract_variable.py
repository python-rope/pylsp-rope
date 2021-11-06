import sys


def main():
    a = int(sys.stdin.read())
    b = 20
    extracted_variable = a + b
    print(extracted_variable)
    c = a + b


a, b = 30, 40
print(a + b)
