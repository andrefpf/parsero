from parsero.token import Token


class TokenList:
    def __init__(self):
        self.tl = []

    def insert(self, token):
        self.tl.append(token)
