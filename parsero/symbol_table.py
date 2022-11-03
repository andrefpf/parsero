from collections import OrderedDict
from tabulate import tabulate


class SymbolTable:
    def __init__(self):
        self.st = OrderedDict()

    def insert(self, symbol, value):
        if symbol not in self.st.keys():
            self.st[symbol] = [len(self.st), value]
            return

    def lookup(self, symbol):
        if symbol in self.st.keys():
            return self.st[symbol]
        raise KeyError("Symbol doesn't exist in Symbol Table.")

    def __str__(self):
        headers = ["index", "symbol", "value"]
        data = []

        for symbol, (index, value) in self.st.items():
            data.append([index, symbol, value])
        
        return tabulate(data, headers=headers, tablefmt="fancy_grid")
