class Table:
    def __init__(self, symbols = {}):
        self.symbols = symbols

    def add(self, symbol):
        self.symbols[symbol.id] = symbol

    def get(self, id):
        if not id in self.symbols:
            print('Undefined symbol', id)
        else:
            return self.symbols[id]

    def update(self, symbol):
        if not symbol.id in self.symbols:
            print('Undefined variable', symbol.id)
        else:
            self.symbols[symbol.id] = symbol

    def print(self):
        print('ID\t', 'TYPE\t', 'VALUE\t', 'LENGTH')
        for s in self.symbols:
            print(s)


class Symbol:
    def __init__(self, id, varType, value, length):
        self.id = id
        self.varType = varType
        self.value = value
        self.length = length