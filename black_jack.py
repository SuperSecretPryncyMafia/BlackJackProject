from flask import Flask


class BlackJack(Flask):
    NAME = "BlackJack"

    def __init__(self):
        super().__init__(self.NAME)
