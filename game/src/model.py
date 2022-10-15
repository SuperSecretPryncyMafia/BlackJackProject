# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten, Dropout, LSTM
import pandas as pd


def preparing_data(dataset: pd.DataFrame):
    # function for reading and extracting training data
    # player_hand;player_options;player_decision;dealer_hand;dealer_options;result
    player_hand = dataset["player_hand"]
    player_sum = dataset["player_options"]
    player_card_no = len(player_hand) - 1
    player_decision = dataset["player_decision"]
    player_visible = player_hand[0]

    dealer_hand = dataset["dealer_hand"]
    dealer_sum = dataset["dealer_options"]
    dealer_card_no = len(dealer_hand) - 1
    dealer_decision = dataset["dealer_decision"]
    dealer_visible = dealer_hand[0]

    # code correct decision for this turn
    result = dataset["result"]
    if result == -1:
        player_decision = int(not player_decision)
    elif result == 2:
        dealer_decision = int(not dealer_decision)


if __name__ == "__main__":
    dataset = pd.read_csv("data_for_nn.txt")
    preparing_data(dataset)
