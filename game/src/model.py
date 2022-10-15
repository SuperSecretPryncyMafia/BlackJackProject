# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten, Dropout, LSTM
import pandas as pd
import numpy as np
from itertools import product
import ast

card_meanings = { "1": [1], "2": [2], "3": [3], "4": [4], "5": [5],
                "6": [6], "7": [7], "8": [8], "9": [9], "10": [10], 
                "J": [10], "Q": [10], "K": [10], "A": [1, 10]}


def preparing_data(dataset: pd.DataFrame):
    # function for reading and extracting training data
    # player_hand;player_options;player_decision;dealer_hand;dealer_options;result

    # decode hands to lists
    player_hand = dataset["player_hand"].to_list()
    player_hand = [ast.literal_eval(x)[:-1] for x in player_hand]

    dealer_hand = dataset["dealer_hand"].to_list()
    dealer_hand = [ast.literal_eval(x)[:-1] for x in dealer_hand]

    # get number of cards in hand for both
    player_card_no = np.array([len(hand) for hand in player_hand])
    dealer_card_no = np.array([len(hand) for hand in dealer_hand])

    # get sums of scores for both
    # and needs of combinations for rest of the arrays
    combinations_dealer = np.ones(len(dealer_hand), dtype=np.int64)
    combinations_player = np.ones(len(player_hand), dtype=np.int64)
    dealer_visible = np.array([])
    dealer_sum = np.array([])
    player_visible = np.array([])
    player_sum = np.array([])

    for i in range(len(dealer_hand)):
        p_sum, p_visible = calc_score(player_hand[i])
        d_sum, d_visible = calc_score(dealer_hand[i])
        p_visible = np.array(p_visible)
        p_sum = np.array(p_sum)
        d_visible = np.array(d_visible)
        d_sum = np.array(d_sum)
        # number of combinations seen by player
        combinations_player[i] = len(d_visible)*len(p_sum)
        # number of combinations seen by dealer
        combinations_dealer[i] = len(p_visible)*len(d_sum)
        # values for player and dealer need to be repeated
        dv = d_visible.shape[0]
        ps = p_sum.shape[0]
        pv = p_visible.shape[0]
        ds = d_sum.shape[0]

        if dv != 1: # player sees ace
            p_sum = np.repeat(p_sum, 2)
        if ps != 1: # player had aces too
            d_visible = np.repeat(d_visible, ps)
        if pv != 1: # dealer sees ace
            d_sum = np.repeat(d_sum, 2)
        if ds != 1: # dealer had aces too
            p_visible = np.repeat(p_visible, ds)
        

        player_visible = np.append(player_visible, p_visible)
        dealer_visible = np.append(dealer_visible, d_visible)
        player_sum = np.append(player_sum, p_sum)
        dealer_sum = np.append(dealer_sum, d_sum)

    player_sum = player_sum.reshape(player_sum.shape[0], -1)
    dealer_sum = dealer_sum.reshape(dealer_sum.shape[0], -1)
    player_visible = player_visible.reshape(player_visible.shape[0], -1)
    dealer_visible = dealer_visible.reshape(dealer_visible.shape[0], -1)

    player_pov = np.append(player_sum, dealer_visible, axis=1)
    dealer_pov = np.append(dealer_sum, player_visible, axis=1)

    # decisions and corrections
    player_decision = dataset["player_decision"].to_numpy()
    dealer_decision = dataset["dealer_decision"].to_numpy()
    result = dataset["result"].to_numpy()
    player_decision[np.where(result == -1)] = np.logical_not(player_decision[np.where(result == -1)])
    dealer_decision[np.where(result == 2)] = np.logical_not(dealer_decision[np.where(result == 2)])

    # repeat the elements in the arrays:
    # decisions, card_no
    own_card_no_for_player = np.repeat(player_card_no, combinations_player)
    own_card_no_for_player = own_card_no_for_player.reshape(own_card_no_for_player.shape[0], -1)
    opp_card_no_for_player = np.repeat(dealer_card_no, combinations_player)
    opp_card_no_for_player = opp_card_no_for_player.reshape(opp_card_no_for_player.shape[0], -1)
    player_decision = np.repeat(player_decision, combinations_player)
    player_decision = player_decision.reshape(player_decision.shape[0], -1)

    player_pov = np.append(player_pov, own_card_no_for_player, axis=1)
    player_pov = np.append(player_pov, opp_card_no_for_player, axis=1)
    player_pov = np.append(player_pov, player_decision, axis=1)

    own_card_no_for_dealer = np.repeat(dealer_card_no, combinations_dealer)
    own_card_no_for_dealer = own_card_no_for_dealer.reshape(own_card_no_for_dealer.shape[0], -1)
    opp_card_no_for_dealer = np.repeat(player_card_no, combinations_dealer)
    opp_card_no_for_dealer = opp_card_no_for_dealer.reshape(opp_card_no_for_dealer.shape[0], -1)
    dealer_decision = np.repeat(dealer_decision, combinations_dealer)
    dealer_decision = dealer_decision.reshape(dealer_decision.shape[0], -1)

    dealer_pov = np.append(dealer_pov, own_card_no_for_dealer, axis=1)
    dealer_pov = np.append(dealer_pov, opp_card_no_for_dealer, axis=1)
    dealer_pov = np.append(dealer_pov, dealer_decision, axis=1)

    ds = np.append(player_pov, dealer_pov, axis=0)
    print(ds.shape)
    return


def calc_score(hand: list) -> list:
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
            summing_array.append(card_meanings[card])

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
        result = [res for res in result if res <= 21]
        visible = summing_array[0]
        return result, visible


if __name__ == "__main__":
    dataset = pd.read_csv("data_for_nn.txt", sep=";")
    preparing_data(dataset)

