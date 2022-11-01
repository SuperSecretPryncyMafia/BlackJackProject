import logging
import threading
import time
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
        self.bot_hand = []
        self.model = None

    def black_jack(self):
        self.generate_deck()
        player_decision = 1
        bot_decision = 1

        self.hit(self.player_hand)
        self.hit(self.bot_hand)

        self.show_game()   # display game

        while True:
            player_decision = self.stay_or_hit_player(player_decision)
            print(player_decision)
            bot_decision = self.stay_or_hit_bot(bot_decision)

            options_player = self.calc_score(self.player_hand)
            options_bot = self.calc_score(self.bot_hand)

            options_bot = [x for x in options_bot if x <= 21]
            options_player = [x for x in options_player if x <= 21]
            # display game
            self.show_game_and_chances(options_player, options_bot)

            if player_decision == 0 and bot_decision == 0:
                result = self.check_when_both_stays(
                    options_player,
                    options_bot
                )
                return result  # result (redirect to result screen)

            result = self.check_if_busted(options_player, options_bot)
            if result != 0:
                return result

    def retrieve_one_card(self):
        self.generate_deck()
        card = sample(self.card_deck, 1)[0]
        self.card_deck.remove(card)
        return {
            "sign": card.sign,
            "value": card.value,
            "color": card.color
        }

    def random_generator_black_jack(self):
        self.generate_deck()
        player_decision = 1
        bot_decision = 1

        self.hit(self.player_hand)
        self.hit(self.bot_hand)
        previous_player_score = self.calc_score(self.player_hand)
        previous_bot_score = self.calc_score(self.bot_hand)

        while True:

            player_decision = self.random_stay_or_hit(
                True,
                player_decision,
                previous_player_score
            )
            bot_decision = self.random_stay_or_hit(
                False,
                bot_decision,
                previous_bot_score
            )

            options_player = self.calc_score(self.player_hand)
            options_bot = self.calc_score(self.bot_hand)

            options_player = [x for x in options_player if x <= 21]
            options_bot = [x for x in options_bot if x <= 21]

            if bot_decision + player_decision == 0:
                result = self.check_when_both_stays_quiet(
                    options_player,
                    options_bot
                )
                self.write_results(
                    previous_player_score,
                    player_decision,
                    previous_bot_score,
                    bot_decision,
                    result
                )
                self.reset()
                return result

            result = self.check_if_busted_quiet(options_player, options_bot)

            self.write_results(
                    previous_player_score,
                    player_decision,
                    previous_bot_score,
                    bot_decision,
                    result
                )

            if result != 0:
                self.reset()
                return result

            previous_player_score = max(options_player)
            previous_bot_score = max(options_bot)

    def stay_or_hit_bot(self, decision):
        if decision == 1:
            current_options = self.calc_score(self.bot_hand)
            current_options = [x for x in current_options if x < 21]

            if len(current_options):
                current_max = max(current_options)
            else:
                return 0

            if current_max <= 16:
                self.hit(self.bot_hand)
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
                    self.hit(self.bot_hand)
            return stay_or_hit[0]
        else:
            return decision

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
        return hand

    def reset(self) -> None:
        """
        We need to reset hands of the bot and the player for the next round
        """
        self.player_hand = []
        self.bot_hand = []

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

    def show_game_and_chances(self, player_chances, bot_chances):
        print("\n")
        print(
            "Player: \n{} --> {}".format(
                [x.sign for x in self.player_hand],
                player_chances
            )
        )
        print(
            "bot: \n{} --> {}".format(
                [x.sign for x in self.bot_hand],
                bot_chances
            )
        )
        print("\n")

    def show_game(self):
        print("\n")
        print("Player: \n{}".format([x.sign for x in self.player_hand]))
        print("bot: \n{}".format([x.sign for x in self.bot_hand]))
        print("\n")

    def write_results(
            self,
            options_player,
            decision_player,
            options_bot,
            decision_bot,
            outcome
            ):

        logging.debug('\n'.join([
            f"Player hand: {[x.sign for x in self.player_hand]}",
            f"Player options: {str(options_player)}",
            f"Player decision: {str(decision_player)}",
            f"\nbot hand: {[x.sign for x in self.bot_hand[:-1]]}",
            f"bot options: {str(options_bot)}",
            f"bot decision: {str(decision_player)}",
            f"\nResult: {str(outcome)}",
            ])
        )
        dataset = [
            str([x.sign for x in self.player_hand]),
            str(options_player),
            str(decision_player),
            str([x.sign for x in self.bot_hand]),
            str(options_bot),
            str(decision_bot),
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
        self.player_decision = 1
        self.bot_decision = 1
        self.player_hand = []
        self.front_end = {}
        super().__init__()

    def spawn_decision_thread(self):
        self.decision_thread = threading.Thread(
            target=self.stay_or_hit_remote,
            args=[]
        )

    def remote_black_jack(self):
        self.prepare_game()
        self.update_frontend()
        result = self.round()
        return result

    def prepare_game(self):
        super().generate_deck()
        self.player_decision = 1
        self.bot_decision = 1
        self.result = 0
        self.player_hand = self.hit(self.player_hand)
        self.bot_hand = self.hit(self.bot_hand)

    @abstractmethod
    def round(self, bot_engine):
        pass

    @abstractmethod
    def stay_or_hit_remote(self):
        pass

    def end_game(self):
        pass

    def hit_player(self):
        # get random card from the deck
        card = sample(self.card_deck, 1)[0]
        self.player_hand.append(card)
        self.card_deck.remove(card)

    def update_frontend(self):
        return self.retrieve_game()

    def retrieve_game(self):
        return {
            "oponent": {
                "cards": [
                    {
                        ''.join([card.sign, card.color]): {
                            "sign": card.sign,
                            "color": card.color,
                            "value": card.value
                        }
                    } for card in self.bot_hand
                ]
            },
            "player": {
                "cards": [
                    {
                        ''.join([card.sign, card.color]): {
                            "sign": card.sign,
                            "color": card.color,
                            "value": card.value
                        }
                    } for card in self.player_hand
                ]
            },
            "result": self.result
        }


class ClassicBlackJack(RemoteBlackJack):
    bot_engine = "Classic"

    def __init__(self):
        super().__init__()

    def stay_or_hit_bot(self, decision):
        return super().stay_or_hit_bot(decision)

    def stay_or_hit_remote(self):
        print("{}: {}".format("self.player_decision", self.player_decision))
        if self.player_decision == 1:
            self.hit_player()
            self.result = self.tour()
        elif self.player_decision == 0:
            self.result = self.tour()
        self.player_decision = None
        return self.update_frontend()

    def round(self):
        while True:
            while not self.decision_made:
                print("Waiting for decision")
                time.sleep(5)
                continue
            else:
                self.decision_made = 0
                self.tour()

    def tour(self):
        self.bot_decision = self.stay_or_hit_bot(self.bot_decision)

        options_player = self.calc_score(self.player_hand)
        options_bot = self.calc_score(self.bot_hand)

        options_bot = [x for x in options_bot if x <= 21]
        options_player = [x for x in options_player if x <= 21]
        # display game
        if self.player_decision == 0 and self.bot_decision == 0:
            result = self.check_when_both_stays(
                options_player,
                options_bot
            )
            return result  # result (redirect to result screen)

        result = self.check_if_busted(options_player, options_bot)
        if result != 0:
            return result


class NeuralBlackJack(ClassicBlackJack):
    bot_engine = "Neural"

    def __init__(self):
        super().__init__()
        self.model = load_model('game/model_file')

    def get_hand_info(self, hand):
        card_no = np.array([len(hand)])
        visible = np.array(hand[0].value)
        options = np.array(self.calc_score(hand))
        return card_no, visible, options

    def if_ace(self, card_no_1, card_no_2, view, ace_no=2):
        card_no_1 = np.repeat(card_no_1, ace_no)
        card_no_2 = np.repeat(card_no_2, ace_no)
        view = np.repeat(view, ace_no)
        return card_no_1, card_no_2, view

    def prepare_data_for_model(self):
        bot_card_no, _, options_bot = self.get_hand_info(self.bot_hand)
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

    def stay_or_hit_bot(self, decision):
        data = self.prepare_data_for_model()
        decisions = self.model.predict(data)
        print(decisions)
        decision = round(np.mean(decisions))
        return decision
