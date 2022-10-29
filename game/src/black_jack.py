import logging
import threading
from abc import abstractmethod
from itertools import product
from random import choices, sample

import numpy as np
from keras.models import load_model


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
        logging.basicConfig(level=logging.ERROR)
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
        # 0 - no decision // 1 - hit // 2 - stand
        self.decision_made = 0
        self.card_deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.model = None

    def black_jack(self):
        self.generate_deck()
        player_decision = 1
        dealer_decision = 1

        self.hit(self.player_hand)
        self.hit(self.dealer_hand)

        self.show_game()   # display game

        while True:
            player_decision = self.stay_or_hit_player(player_decision)
            print(player_decision)
            dealer_decision = self.stay_or_hit_dealer(dealer_decision)

            options_player = self.calc_score(self.player_hand)
            options_dealer = self.calc_score(self.dealer_hand)

            options_dealer = [x for x in options_dealer if x <= 21]
            options_player = [x for x in options_player if x <= 21]
            # display game
            self.show_game_and_chances(options_player, options_dealer)

            if player_decision == 0 and dealer_decision == 0:
                result = self.check_when_both_stays(
                    options_player,
                    options_dealer
                )
                return result  # result (redirect to result screen)

            result = self.check_if_busted(options_player, options_dealer)
            if result != 0:
                return result

    def remote_black_jack(self):
        game_state = self.retrieve_start()
        player_decision = game_state["player"]["decision"]
        dealer_decision = game_state["oponent"]["decision"]
        result = 0
        while True:
            game_state = self.get_game_state()  # and add request
            self.decision_made = game_state["player"]["decision_made"]

            while not self.decision_made:
                game_state = self.get_game_state()
                self.player_decision = self.decision_made - 1
                # player_decision = game_state["player"]["decision"]
                # another option
                # self.decision_made = game_state["player"]["decision_made"]
            else:
                # print(player_decision)
                # they shouldnt change on the other side of the program
                # probably unnecessary
                # self.player_hand = [Card(
                #     card["sign"],
                #     card["value"],
                #     card["color"]
                # ) for card in game_state["player"]["hand"]]
                # self.dealer_hand = [
                #     Card(card["sign"],
                #     card["value"],
                #     card["color"]
                # ) for card in game_state["dealer"]["hand"]]
                # if self.model is not None:
                #     data = self.prepare_data_for_model()
                #     dealer_decision = round(np.mean(
                #         self.model.predict(data)))
                # else:
                #     # Sperate version for model (reading js, earlier setup)
                options_player = self.calc_score(self.player_hand)
                options_dealer = self.calc_score(self.dealer_hand)

                options_dealer = [x for x in options_dealer if x <= 21]
                options_player = [x for x in options_player if x <= 21]

                dealer_decision = self.stay_or_hit_dealer(dealer_decision)

                self.decision_made = 0
                if player_decision == 0 and dealer_decision == 0:
                    result = self.check_when_both_stays(
                        options_player,
                        options_dealer
                    )
                    self.decision_thread.join()
                    return result

                result = self.check_if_busted(options_player, options_dealer)
                if result != 0:
                    self.decision_thread.join()
                    return result

        self.decision_thread.join()
        #     options_player = self.calc_score(self.player_hand)
        #     options_dealer = self.calc_score(self.dealer_hand)

        #     options_dealer = [x for x in options_dealer if x <= 21]
        #     options_player = [x for x in options_player if x <= 21]

        #     self.show_game_and_chances(options_player, options_dealer)

        #     if player_decision == 0 and dealer_decision == 0:
        #         result = self.check_when_both_stays(
        #             options_player,
        #             options_dealer
        #         )
        #         return result

        #     result = self.check_if_busted(options_player, options_dealer)
        #     if result != 0:
        #         return result

    def stay_or_hit_remote(self):
        while True:
            if self.decision_made == 0:
                pass

    def retrieve_one_card(self):
        self.generate_deck()
        card = sample(self.card_deck, 1)[0]
        self.card_deck.remove(card)
        return {
            "sign": card.sign,
            "value": card.value,
            "color": card.color
        }

    def retrieve_start(self):
        player_decision, dealer_decision = self.prepare_game()
        return {
            "oponent": {
                "decision": dealer_decision,
                "cards": [
                    {
                        card: {
                            "sign": card.sign,
                            "color": card.color,
                            "value": card.value
                        }
                    } for card in self.dealer_hand
                ]
            },
            "player": {
                "decision_made": 0,
                "decision": player_decision,
                "cards": [
                    {
                        card: {
                            "sign": card.sign,
                            "color": card.color,
                            "value": card.value
                        }
                    } for card in self.player_hand
                ]
            }
        }

    def retrieve_game(self, player_chances, oponent_chances):
        return {
            "oponent": {
                "cards": [
                    {
                        card: {
                            "sign": card.sign,
                            "color": card.color,
                            "value": card.value
                        }
                    } for card in self.dealer_hand
                ],
                "score": max(oponent_chances)
            },
            "player": {
                "decision_made": 0,
                "cards": [
                    {
                        card: {
                            "sign": card.sign,
                            "color": card.color,
                            "value": card.value
                        }
                    } for card in self.dealer_hand
                ],
                "score": max(player_chances)
            }
        }

    def get_game_state(self):
        return

    def random_generator_black_jack(self):
        self.generate_deck()
        player_decision = 1
        dealer_decision = 1

        self.hit(self.player_hand)
        self.hit(self.dealer_hand)
        previous_player_score = self.calc_score(self.player_hand)
        previous_dealer_score = self.calc_score(self.dealer_hand)

        while True:

            player_decision = self.random_stay_or_hit(
                True,
                player_decision,
                previous_player_score
            )
            dealer_decision = self.random_stay_or_hit(
                False,
                dealer_decision,
                previous_dealer_score
            )

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
                    dealer_decision,
                    result
                )
                self.reset()
                return result

            result = self.check_if_busted_quiet(options_player, options_dealer)

            self.write_results(
                    previous_player_score,
                    player_decision,
                    previous_dealer_score,
                    dealer_decision,
                    result
                )

            if result != 0:
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

    def random_stay_or_hit(
            self,
            player: bool,
            decision: int,
            previous_score: int = 0
            ) -> int:
        if previous_score == 21:
            return 0
        if decision:
            stay_or_hit = choices([0, 1], weights=(1, 3), k=1)
            if stay_or_hit:
                if player:
                    self.hit(self.player_hand)
                else:
                    self.hit(self.dealer_hand)
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
            decision_dealer,
            outcome
            ):

        logging.debug('\n'.join([
            f"Player hand: {[x.sign for x in self.player_hand]}",
            f"Player options: {str(options_player)}",
            f"Player decision: {str(decision_player)}",
            f"\nDealer hand: {[x.sign for x in self.dealer_hand[:-1]]}",
            f"Dealer options: {str(options_dealer)}",
            f"Dealer decision: {str(decision_player)}",
            f"\nResult: {str(outcome)}",
            ])
        )
        dataset = [
            str([x.sign for x in self.player_hand]),
            str(options_player),
            str(decision_player),
            str([x.sign for x in self.dealer_hand]),
            str(options_dealer),
            str(decision_dealer),
            str(outcome),
            "\n"
        ]

        with open("data_for_nn.txt", "a+") as file:
            string = ";".join(dataset)
            file.write(string)

    def generate_deck(self):
        for sign in self.deck_template.keys():
            for color in self.deck_template[sign]["color"]:
                self.card_deck.append(
                    Card(sign, self.deck_template[sign]["value"], color)
                )


class Card:
    def __init__(self, sign: str, value: list, color: str):
        self.sign = sign
        self.value = value
        self.color = color


class RemoteBlackJack(Game):
    def __init__(self):
        self.decision_thread = None
        super().__init__()

    def spawn_decision_thread(self):
        self.decision_thread = threading.Thread(
            target=self.stay_or_hit_remote,
            args=[]
        )

    def remote_black_jack(self):
        player_decision, bot_decision = self.prepare_game()
        self.update_frontend()
        result = self.round()

    def prepare_game(self):
        super().generate_deck()
        player_decision = 1
        dealer_decision = 1
        self.hit(self.player_hand)
        self.hit(self.dealer_hand)

        return player_decision, dealer_decision

    @abstractmethod
    def round(self, bot_engine):
        pass

    def stay_or_hit_remote(self, decision):
        pass

    def update_frontend(self):
        pass


class NeuralBlackJack(RemoteBlackJack):
    bot_engine = "Neural"

    def __init__(self):
        super().__init__()
        self.model = load_model('game/model_file')

    def get_hand_info(self, hand):
        card_no = np.array([len(hand)])
        visible = np.array(hand[0].value)
        options = self.calc_score(hand)
        return card_no, visible, options

    def if_ace(self, card_no_1, card_no_2, view, ace_no=2):
        card_no_1 = np.repeat(card_no_1, ace_no)
        card_no_2 = np.repeat(card_no_2, ace_no)
        view = np.repeat(view, ace_no)
        return card_no_1, card_no_2, view

    def prepare_data_for_model(self):
        bot_card_no, _, options_bot = self.get_hand_info(self.dealer_hand)
        player_card_no, player_view, _ = self.get_hand_info(self.player_hand)

        pv = player_view.shape[0]
        od = options_bot.shape[0]
        if pv != 1:  # if player has visible ace
            player_card_no, bot_card_no, options_bot = self.if_ace(
                player_card_no,
                bot_card_no,
                options_bot
            )
        if od != 1:  # dealer has aces too
            player_card_no, bot_card_no, player_view = self.if_ace(
                player_card_no,
                bot_card_no,
                player_view,
                od
            )

        data = options_bot.reshape(options_bot.shape[0], -1)

        for column in [player_view, bot_card_no, player_card_no]:
            column = column.reshape(column.shape[0], -1)
            data = np.append(data, column, axis=1)

        data = data/np.array([20, 10, 8, 8])
        return data

    def stay_or_hit_dealer(self, decision):
        data = self.prepare_data_for_model()
        decision = round(np.mean(
            self.model.predict(data)))
        return decision

    def round(self):
        pass


class ClassicBlackJack(RemoteBlackJack):
    bot_engine = "Classic"

    def __init__(self):
        super().__init__()

    def stay_or_hit_dealer(self, decision):
        return super().stay_or_hit_dealer(decision)

    def round(self):
        while True:
            while not self.decision_made:
                continue
            else:
                self.decision_made = 0
                self.tour()

    def tour(self):
        pass


if __name__ == "__main__":
    black_jack = Game()
    listner = threading.Thread(
        target=black_jack.stay_or_hit_remote
    )
