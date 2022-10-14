import pandas as pd
# import numpy as np

deck = []

# Loading data
dataset = pd.read_csv("data_for_nn.txt")

# Working on the copy of the original data
dataframe = dataset.copy()

# Getting rid of unnecessary data
dataframe = dataframe.drop(columns=["None"])
print(dataframe.info())

# Dividing data into separate cases with respect to the "Result" column
only_win_df = dataframe[dataframe["Result"] == 2]
only_tie_df = dataframe[dataframe["Result"] == 1]
only_lose_df = dataframe[dataframe["Result"] == -1]

# Counting the dealer card at the separate cases
dealer_card_win = {'A': 7749, '2': 20779, '3': 22391, '4': 23974, '5': 25354, '6': 27319, '7': 20073, '8': 18999, '9': 17633, '10': 14245, 'J': 14436, 'Q': 14292, 'K': 14348}
dealer_card_tie = {'A': 4761, '2': 9249, '3': 10312, '4': 11345, '5': 12516, '6': 13762, '7': 9402, '8': 9136, '9': 8863, '10': 8795, 'J': 8903, 'Q': 8753, 'K': 8966}
dealer_card_lose = {'A': 64557, '2': 46651, '3': 44078, '4': 41845, '5': 39034, '6': 36259, '7': 47289, '8': 48535, '9': 50349, '10': 54226, 'J': 54017, 'Q': 53710, 'K': 53762}

print()
print("Sorted hand of the dealer at cases from most frequent to the least frequent:")
print("Cards of the dealer when match is won:")
print(sorted(dealer_card_win.items(), key=lambda x: x[1], reverse=True))

print("Cards of the dealer when match is tied:")
print(sorted(dealer_card_tie.items(), key=lambda x: x[1], reverse=True))

print("Cards of the dealer when match is lost:")
print(sorted(dealer_card_lose.items(), key=lambda x: x[1], reverse=True))
print()

# Counting how many cases of winning,ties ,or losing is in our dataset
nr_of_win = len(only_win_df.index)
nr_of_tie = len(only_tie_df.index)
nr_of_lose = len(only_lose_df.index)

# Calculating total number of samples
total = nr_of_win + nr_of_tie + nr_of_lose

print("Percentage of wins: " + str((nr_of_win/total)*100)[:5] + " %")
print("Percentage of tie: " + str((nr_of_tie/total)*100)[:5] + " %")
print("Percentage of lose: " + str((nr_of_lose/total)*100)[:5] + " %")

print("Percentage of non-negative outcome: " + str(
    ((nr_of_tie+nr_of_win)/total)*100)[:5] + " %"
)

print("Winning case analysis: ")
