from Collections import OrderedDict


class SymbolTable:
    def __init__(self):
        st = OrderedDict()

    self insert(self, symbol, value):
        if symbol not in self.st.keys():
            st[symbol] = [len(st), value]
            return
        raise KeyError("Symbol already exists in Symbol Table.")
    
    self lookup(self, symbol):
        if symbol in self.st.keys():
            return st[symbol]
        raise KeyError("Symbol doesn't exist in Symbol Table.")