import black_jack


if __name__ == "__main__":
    game = black_jack.Game()
    game.generate_deck()
    deck = [
        "Sign: {}\tValue: {}\tColor: {}\n".format(
            *[x.sign, x.value, x.color]
        ) for x in game.card_deck
    ]
    for card in deck:
        print(card)
    game.random_generator_black_jack()
