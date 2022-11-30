from parsero import Parser

a = 123

def function():
    def subfunction(x):
        for i in range(x):
            print("ueepa")  

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