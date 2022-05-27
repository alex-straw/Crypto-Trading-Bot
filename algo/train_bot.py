import pandas as pd
from numpy import concatenate
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.tree import DecisionTreeRegressor

pd.options.mode.chained_assignment = None  # default='warn'


def add_future_price(df, n_steps_ahead):
    """ Get future price change for training labels """
    df['shifted_market_price'] = df['market_price'].shift(periods=n_steps_ahead)
    df = df.iloc[n_steps_ahead:]  # Skip NaNs
    df['future_price_change_pct'] = (df['shifted_market_price'] - df['market_price']) / df['market_price']

    return df


def get_x_y(df):
    x_cols = [col for col in df if col.startswith('bid') or col.startswith('ask')]
    x_data = df[x_cols]
    y_data = df['future_price_change_pct']

    return x_data, y_data


def get_train_test_split(train_size, df):
    """
    Splits data frame into test and train (chronologically)
    """
    split_idx = int(train_size * df.shape[0])
    train = df.iloc[0:split_idx]
    test = df.iloc[split_idx:-1]

    return train, test


def plot_model(y_test_pred, y_test_true, model):
    fig, ax = plt.subplots(figsize=(20, 6))

    time_data = y_test_true.index

    datapoint_index = range(0, len(time_data))

    ax.plot(datapoint_index, y_test_pred, label='predicted change over next 30 seconds')
    ax.plot(datapoint_index, y_test_true, label='actual change over next 30 seconds')
    ax.grid()
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Change (%)')
    plt.title(model)
    plt.savefig(f'output_images/{model}.png')


def main():

    train_size = 0.8
    n_steps_ahead = 6

    feature_df = pd.read_csv('output_data/saved_data/BTC-USD-700.csv')
    feature_df = feature_df.drop(feature_df.columns[0], axis=1)  # Drop original index column
    feature_df['time'] = pd.to_datetime(feature_df['time'], unit='s')
    feature_df.set_index('time', inplace=True, drop=True)

    feature_df = add_future_price(feature_df, n_steps_ahead)

    train, test = get_train_test_split(train_size, feature_df)

    x_data_train, y_data_train = get_x_y(train)
    x_data_test, y_data_test = get_x_y(test)

    linear_reg_model = LinearRegression().fit(x_data_train, y_data_train)

    y_data_pred = linear_reg_model.predict(x_data_test)

    print(mean_squared_error(y_data_pred, y_data_test))
    plot_model(y_data_pred, y_data_test, 'Linear Regression')


if __name__ == "__main__":
    main()