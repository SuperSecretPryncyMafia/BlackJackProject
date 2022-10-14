# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten, Dropout, LSTM
import pandas as pd


def preparing_data(dataset: pd.DataFrame):
    # results = dataset["Result"]
    # score = dataset["Score"]
    # dealer = dataset["Dealer"]
    decision = dataset["Decision"]

    print(decision)


if __name__ == "__main__":
    dataset = pd.read_csv("data_for_nn.txt")
    preparing_data(dataset)
