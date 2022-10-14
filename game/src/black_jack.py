from random import choices, sample
from itertools import product


class Game:
    """
    Game class possesses all necessary elements of the black jack game
    with two modes, one the game and second the generator.
    In game mode user is the player and has console output.
    In generator mode there is no printing, just
    writing data about the match to the file.

    :param id: id for the text file (index)
    """
    def __init__(self):
        self.colors = ["clubs", "diamonds", "spades", "hearts"]
        self.deck_template = {
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
        self.card_deck = []
        self.player_hand = []
        self.dealer_hand = []

    def black_jack(self):
        self.generate_deck()
        player_decision = 1
        dealer_decision = 1

        self.hit(self.player_hand)
        self.hit(self.dealer_hand)

        self.show_game()

        while True:
            player_decision = self.stay_or_hit_player(player_decision)
            print(player_decision)
            dealer_decision = self.stay_or_hit_dealer(dealer_decision)

            options_player = self.calc_score(self.player_hand)
            options_dealer = self.calc_score(self.dealer_hand)

            options_dealer = [x for x in options_dealer if x <= 21]
            options_player = [x for x in options_player if x <= 21]

            self.show_game_and_chances(options_player, options_dealer)

            if player_decision == 0 and dealer_decision == 0:
                result = self.check_when_both_stays(
                    options_player,
                    options_dealer
                )
                return result

            result = self.check_if_busted(options_player, options_dealer)
            if result != 0:
                return result

    def random_generator_black_jack(self):
        self.generate_deck()
        player_decision = 1
        dealer_decision = 1

        self.hit(self.player_hand)
        self.hit(self.dealer_hand)
        previous_player_score = self.calc_score(self.player_hand)
        previous_dealer_score = self.calc_score(self.dealer_hand)

        while True:
            """
            Decyzja zostaje blokowana w momencie gry gracz ma 21 (stay)
            """

            player_decision = self.random_stay_or_hit(player_decision)
            dealer_decision = self.random_stay_or_hit(dealer_decision)

            options_player = self.calc_score(self.player_hand)
            options_dealer = self.calc_score(self.dealer_hand)

            options_player = [x for x in options_player if x <= 21]
            options_dealer = [x for x in options_dealer if x <= 21]

            if dealer_decision + player_decision == 0:
                result = self.check_when_both_stays_quiet(
                    options_player,
                    options_dealer
                )
                self.write_results(
                    previous_player_score,
                    player_decision,
                    previous_dealer_score,
                    result
                )
                self.reset()
                return result

            result = self.check_if_busted_quiet(options_player, options_dealer)
            if result != 0:
                self.write_results(
                    previous_player_score,
                    player_decision,
                    previous_dealer_score,
                    result
                )
                self.reset()
                return result

            previous_player_score = max(options_player)
            previous_dealer_score = max(options_dealer)

    def stay_or_hit_dealer(self, decision):
        if decision == 1:
            current_options = self.calc_score(self.dealer_hand)
            current_options = [x for x in current_options if x < 21]

            if len(current_options):
                current_max = max(current_options)
            else:
                return 0

            if current_max <= 16:
                self.hit(self.dealer_hand)
                return 1
            elif current_max > 16:
                return 0
        else:
            return decision

    def random_stay_or_hit(self, decision: int) -> int:
        if decision:
            stay_or_hit = choices([0, 1], weights=(1, 3), k=1)
            if stay_or_hit:
                self.hit(self.player_hand)
            return stay_or_hit[0]
        else:
            return decision

    def weighted_random_stay_or_hit(self, decision: int) -> int:
        pass

    def stay_or_hit_player(self, decision):
        try:
            if decision:
                stay_or_hit = int(input("Stay: 0\nHit: 1\n"))
                print(stay_or_hit)
                if stay_or_hit:
                    self.hit(self.player_hand)
                decision = stay_or_hit
        except ValueError:
            print("You need to enter the digit 0 or 1")
            decision = self.stay_or_hit_player(decision)
        finally:
            return decision

    def hit(self, hand):
        # get random card from the deck
        card = sample(self.card_deck, 1)[0]
        hand.append(card)
        self.card_deck.remove(card)

    def reset(self) -> None:
        """
        We need to reset hands of the dealer and the player for the next round
        """
        self.player_hand = []
        self.dealer_hand = []

    def calc_score(self, hand: list) -> list:
        """
        We need to translate the cards from hand to the appropriate scores
        basing on the values of the cards. Important case is when in our
        hand is ace which posses two different scores ( 1 and 10 ).
        Because of this we need to create two possible outcomes.
        Number of outcomes increase when we have more than one ace in our hand.
        Example: hand( A, A ) --> outcomes( 2, 11, 11, 20 )
        We also get rid of the duplicates from the outcomes so the final
        returned list would look like this --> outcomes( 2, 11, 20 )
        When another card will land in our hand, for example 3 then all of
        our outcomes will increase by 3.

        param hand - list of cards in the hand
        return - list of possible scores from that hand
        """
        summing_array = []
        result = [0]

        # Translating cards to numbers
        for card in hand:
            summing_array.append(card.value)

        # Summing the result
        for points in summing_array:
            # This part of code takes care of the Ace which
            # has two possible values
            if len(points) > 1:
                # Generating permutation of the values from result and from
                # point with summing
                all_results = [sum(x) for x in list(product(result, points))]
                # As all the values are inside of the permutation we can reset
                # result for new values
                result = []
                # Getting rid of the duplicates
                for value in all_results:
                    if value not in result:
                        result.append(value)
            else:
                # If we have single valued card then just sum to all possible
                # results from result
                for i, possibility in enumerate(result):
                    possibility += points[0]
                    result[i] = possibility

        return result

    @staticmethod
    def check_if_busted(options_p, options_d):
        if len(options_p) == 0:
            if len(options_d) == 0:
                print("Tie")
                return 1
            else:
                print("You lose")
                return -1
        elif len(options_d) == 0:
            print("You win")
            return 2
        return 0

    @staticmethod
    def check_if_busted_quiet(options_p, options_d):
        if len(options_p) == 0:
            if len(options_d) == 0:
                return 1
            else:
                return -1
        elif len(options_d) == 0:
            return 2
        return 0

    @staticmethod
    def check_when_both_stays(options_p, options_d):
        max_p = max(options_p)
        max_d = max(options_d)
        if max_p > max_d:
            print("Wou win")
            return 2
        elif max_p < max_d:
            print("You loose")
            return -1
        else:
            print("Tie")
            return 1

    @staticmethod
    def check_when_both_stays_quiet(options_p, options_d):
        if len(options_p) == 0 and len(options_d) == 0:
            return 1
        elif len(options_p) == 0:
            return -1
        elif len(options_d) == 0:
            return 2

        max_p = max(options_p)
        max_d = max(options_d)
        if max_p > max_d:
            return 2
        elif max_p < max_d:
            return -1
        else:
            return 1

    def show_game_and_chances(self, player_chances, dealer_chances):
        print("\n")
        print(
            "Player: \n{} --> {}".format(
                [x.sign for x in self.player_hand],
                player_chances
            )
        )
        print(
            "Dealer: \n{} --> {}".format(
                [x.sign for x in self.dealer_hand],
                dealer_chances
            )
        )
        print("\n")

    def show_game(self):
        print("\n")
        print("Player: \n{}".format([x.sign for x in self.player_hand]))
        print("Dealer: \n{}".format([x.sign for x in self.dealer_hand]))
        print("\n")

    def write_results(
            self,
            options_player,
            decision_player,
            options_dealer,
            outcome
            ):

        # print(
        #     "Player hand: ", [x.sign for x in self.player_hand],
        #     "\nPlayer options: ", str(options_player),
        #     "\nPlayer decision: ", str(decision_player),
        #     "\n\nDealer hand: ", [x.sign for x in self.dealer_hand[:-1]],
        #     "\nDealer options: ", str(options_dealer),
        #     "\n\nResult: ", str(outcome)
        # )
        dataset = [
            str([x.sign for x in self.player_hand]),
            str(options_player),
            str(decision_player),
            str([x.sign for x in self.dealer_hand[:-1]]),
            str(options_dealer),
            str(outcome),
            "\n"
        ]

        with open("data_for_nn_test.txt", "a+") as file:
            string = ";".join(dataset)
            file.write(string)

    def generate_deck(self):
        for sign in self.deck_template.keys():
            for color in self.deck_template[sign]["color"]:
                self.card_deck.append(
                    Card(sign, self.deck_template[sign]["value"], color)
                )

class Player:
    pass

class Bot:
    pass

class Dealer(Bot):
    pass



class Card:
    def __init__(self, sign: str, value: list, color: str):
        self.sign = sign
        self.value = value
        self.color = color
