# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten, Dropout, LSTM
from sklearn.model_selection import train_test_split
import numpy as np


if __name__ == "__main__":
    print("model file, nothing tu see here yet ")
    data = np.loadtxt("raw_data.csv", delimiter=',')
    X = data[:, :-1]
    X = X/np.array([20, 10, 8, 8])
    y = data[:, -1]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, 
        random_state=42, stratify=y)
    X_train, X_test, y_train, y_test = train_test_split(
        X_train, y_train, test_size=0.125, 
        random_state=42, stratify=y_train)
