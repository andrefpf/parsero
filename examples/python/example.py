from parsero import Parser

a = 123


class Test:
    def __init__(self, hello):
        pass


def function():
    def _subfunction(x):
        for i in range(10):
            print("ueepa")  
        a = 3
        return 2

    listinha = [1, "2", "três"]

    for i in listinha:
        print(i)

    while True:
        subfunction(10)

    if a > 0:
        print("maior")
    elif a < 0:
        print("menor")
    else:
        print(igual)