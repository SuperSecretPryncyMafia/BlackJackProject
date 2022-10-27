from random import choices, sample
from itertools import product
import logging
import threading
import requests
import numpy as np


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
        self.decision_thread = threading.Thread(target=self.stay_or_hit_remote, args=[])
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

            self.show_game_and_chances(options_player, options_dealer)  # display game

            if player_decision == 0 and dealer_decision == 0:
                result = self.check_when_both_stays(
                    options_player,
                    options_dealer
                )
                return result  # result (redirect to result screen)

            result = self.check_if_busted(options_player, options_dealer)
            if result != 0:
                return result

    def prepare_game(self):
        self.generate_deck()
        player_decision = 1
        dealer_decision = 1
        self.hit(self.player_hand)
        self.hit(self.dealer_hand)

        return player_decision, dealer_decision

    def remote_black_jack(self):
        self.decision_thread.start()
        game_state = self.retrieve_start()
        player_decision = game_state["player"]["decision"]
        dealer_decision = game_state["oponent"]["decision"]
        result = 0
        while True:
            game_state = self.get_game_state() # and add request
            self.decision_made = game_state["player"]["decision_made"]

            while not self.decision_made:
                game_state = self.get_game_state()
                player_decision = self.stay_or_hit_player(player_decision)
                # player_decision = game_state["player"]["decision"] # another option
                self.decision_made = game_state["player"]["decision_made"]
            else:
                print(player_decision)
                # they shouldnt change on the other side of the program, so probably unnecessary
                # self.player_hand = [Card(card["sign"], 
                #     card["value"], card["color"]) for card in game_state["player"]["hand"]]
                # self.dealer_hand = [Card(card["sign"], 
                #     card["value"], card["color"]) for card in game_state["dealer"]["hand"]]
                if self.model is not None:
                    data = self.prepare_data_for_model()
                    dealer_decision = round(np.mean(
                        self.model.predict(data)))
                else:
                    dealer_decision = self.stay_or_hit_dealer(dealer_decision) # Sperate version for model (reading js, earlier setup)
                self.decision_made = 0
            if result:
                break

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

    def prepare_data_for_model(self):
        opponent_card_no = np.array([len(self.player_hand)])
        dealer_card_no = np.array([len(self.dealer_hand)])
        opponent_visible = np.array(self.player_hand[0].value)
        options_dealer = self.calc_score(self.dealer_hand)
        options_dealer = np.array([x for x in options_dealer if x <= 21])

        ov = opponent_visible.shape[0]
        od = options_dealer.shape[0]
        if ov != 1: # if player has visible ace
            opponent_card_no = np.repeat(opponent_card_no, 2)
            dealer_card_no = np.repeat(dealer_card_no, 2)
            options_dealer = np.repeat(options_dealer, 2)
        if od != 1: # dealer has aces too
            opponent_visible = np.repeat(opponent_visible, od)
            dealer_card_no = np.repeat(dealer_card_no, od)
            opponent_card_no = np.repeat(opponent_card_no, od)

        opponent_card_no = opponent_card_no.reshape(
            opponent_card_no[0], -1) 
        dealer_card_no = dealer_card_no.reshape(
            dealer_card_no[0], -1) 
        opponent_visible = opponent_visible.reshape(
            opponent_visible.shape[0], -1)
        options_dealer = options_dealer.reshape(
            options_dealer.shape[0], -1
        )
        data = np.append(options_dealer, 
            opponent_visible, axis=1)
        data = np.append(data,
            dealer_card_no, axis=1)
        data = np.append(data, 
            opponent_card_no, axis=1)

        data = data/np.array([20, 10, 8, 8])
        return data

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


if __name__=="__main__":
    listner = threading.Thread(target=get_decision)