
class DeckTemplate:
    def __init__(self, colors):
        self.colors = colors
        return{
            "2": {
                "value": [2],
                "color": self.colors
            },
            "3": {
                "value": [3],
                "color": self.colors
            },
            "4": {
                "value": [4],
                "color": self.colors
            },
            "5": {
                "value": [5],
                "color": self.colors
            },
            "6": {
                "value": [6],
                "color": self.colors
            },
            "7": {
                "value": [7],
                "color": self.colors
            },
            "8": {
                "value": [8],
                "color": self.colors
            },
            "9": {
                "value": [9],
                "color": self.colors
            },
            "10": {
                "value": [10],
                "color": self.colors
            },
            "J": {
                "value": [10],
                "color": self.colors
            },
            "Q": {
                "value": [10],
                "color": self.colors
            },
            "K": {
                "value": [10],
                "color": self.colors
            },
            "A": {
                "value": [1, 10],
                "color": self.colors
            }
        }
