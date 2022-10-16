from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.constraints import MaxNorm
from tensorflow.keras.optimizers import Adam
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
    
    callback = EarlyStopping(monitor='val_accuracy', patience=10, verbose=True)
    adam = Adam(learning_rate=0.001)

    model = Sequential()
    model.add(Dropout(0.2, input_shape=(X.shape[1],)))
    model.add(Dense(100, activation="relu",
        kernel_constraint=MaxNorm(3)))
    model.add(Dropout(0.2))
    model.add(Dense(50, activation="relu", 
        kernel_constraint=MaxNorm(3)))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', 
        optimizer=adam, metrics=['accuracy'])

    history = model.fit(X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100, batch_size=16, callbacks=[callback],
        verbose=1)
    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Baseline Error: %.2f%%" % (100-scores[1]*100))
    model.save('game/model_file')