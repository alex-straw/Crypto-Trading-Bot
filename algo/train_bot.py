import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from numpy import concatenate


def add_future_price(df, n_steps_ahead):
    """ Get future price change for training labels """
    df['shifted_market_price'] = df['market_price'].shift(periods=n_steps_ahead)
    df = df.iloc[n_steps_ahead:]  # Skip NaNs
    df['future_price_change_pct'] = (df['shifted_market_price'] - df['market_price']) / df['market_price']*100

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


def main():

    train_size = 0.8

    feature_df = pd.read_csv('output_data/BTC-USD_data.csv')
    feature_df = feature_df.drop(feature_df.columns[0], axis=1)  # Drop original index column
    feature_df.set_index('time', inplace=True, drop=True)

    feature_df = add_future_price(feature_df, n_steps_ahead=6)

    test, train = get_train_test_split(train_size, feature_df)

    x_data_train, y_data_train = get_x_y(train)
    x_data_test, y_data_test = get_x_y(test)


if __name__ == "__main__":
    main()