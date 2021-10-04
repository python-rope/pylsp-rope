def add(a, b):
    return NewMethodObject(a, b)()


class NewMethodObject(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        print(f"{self.a} + {self.b} = {self.a + self.b}")
        return self.a + self.b
