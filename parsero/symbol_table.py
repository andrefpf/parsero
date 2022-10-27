from Collections import OrderedDict


class SymbolTable:
    def __init__(self):
        self.st = OrderedDict()

    def insert(self, symbol, value):
        if symbol not in self.st.keys():
            self.st[symbol] = [len(self.st), value]
            return
        raise KeyError("Symbol already exists in Symbol Table.")

    def lookup(self, symbol):
        if symbol in self.st.keys():
            return self.st[symbol]
        raise KeyError("Symbol doesn't exist in Symbol Table.")
