import sys


class MyClass:
    def my_method(self):
        self.local_var = 10
        print(sys.stdin.read())
        print(self.local_var)
