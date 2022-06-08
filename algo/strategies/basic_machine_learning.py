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


def plot_model(y_test_pred, y_test_true, model, n_steps_ahead):
    fig, ax = plt.subplots(figsize=(20, 6))

    interval = 5
    time_data = y_test_true.index

    total_time = len(time_data)*interval

    market_price_indices = range(0, total_time, interval)

    x = np.linspace(0, total_time, 5)
    y = [0] * x.shape[0]

    ax.plot(market_price_indices, y_test_pred, label='Predicted price change over next 30 seconds')
    ax.plot(market_price_indices, y_test_true, label='Actual price change over next 30 seconds')

    ax.plot(x, y, color='red')
    ax.grid()
    ax.legend()
    ax.set_xlabel('Time (Seconds)')
    ax.set_ylabel('Change (%)')
    plt.xticks(range(0, len(time_data)*interval, interval*n_steps_ahead))
    plt.title(model)
    plt.savefig(f'../output_images/{model}.png')


def max_depth_testing(x_data_train, y_data_train, x_data_val, y_data_val):

    results = {
        'depth_values': range(1, 20),
        'error': []
    }

    for depth in results['depth_values']:
        dtr_model = DecisionTreeRegressor(max_depth=depth).fit(x_data_train, y_data_train)
        y_pred_val = dtr_model.predict(x_data_val)
        results['error'].append(mean_squared_error(y_pred_val, y_data_val, squared=False))

    fig, ax = plt.subplots()
    ax.plot(results['depth_values'], results['error'])
    ax.set_xlabel('max depth')
    ax.set_ylabel('MSE')
    plt.show()


def main():

    train_size = 0.8
    n_steps_ahead = 10

    feature_df = pd.read_csv('../output_data/BTC-USD_data.csv')
    feature_df = feature_df.drop(feature_df.columns[0], axis=1)  # Drop original index column
    feature_df['time'] = pd.to_datetime(feature_df['time'], unit='s')
    feature_df.set_index('time', inplace=True, drop=True)

    feature_df = add_future_price(feature_df, n_steps_ahead)

    train, test = get_train_test_split(train_size, feature_df)
    train, val = get_train_test_split(train_size, train)

    x_data_train, y_data_train = get_x_y(train)
    x_data_test, y_data_test = get_x_y(test)
    x_data_val, y_data_val = get_x_y(val)

    linear_reg_model = LinearRegression().fit(x_data_train, y_data_train)
    dtr_model = DecisionTreeRegressor(max_depth=6).fit(x_data_train, y_data_train)

    max_depth_testing(x_data_train, y_data_train, x_data_val, y_data_val)  # Best turned out to be 6

    y_data_pred = linear_reg_model.predict(x_data_test)
    y_data_pred_dtr = dtr_model.predict(x_data_test)

    plot_model(y_data_pred, y_data_test, 'linear_regression', n_steps_ahead)
    plot_model(y_data_pred_dtr, y_data_test, 'linear_regression', n_steps_ahead)


if __name__ == "__main__":
    main()