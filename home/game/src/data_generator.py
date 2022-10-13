import black_jack

if __name__ == "__main__":
    BlackJack = black_jack.Game()
    number_of_repetitions = 100000
    i = 0
    while i < number_of_repetitions:
        if i % 1000 == 0:
            BlackJack = black_jack.Game()
        BlackJack.random_generator_black_jack()
        i += 1
