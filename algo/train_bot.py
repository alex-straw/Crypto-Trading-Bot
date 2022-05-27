import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def add_future_price(df, n_steps_ahead):
    """ Get future price change for training labels """
    df['shifted_market_price'] = df['market_price'].shift(periods=n_steps_ahead)
    df = df.iloc[n_steps_ahead:]  # Skip NaNs
    df['future_price_change'] = (df['shifted_market_price'] - df['market_price']) / df['market_price']

    return df


def main():

    feature_df = pd.read_csv('output_data/BTC-USD_data.csv')
    feature_df = feature_df.drop(feature_df.columns[0], axis=1)  # Drop original index column
    feature_df.set_index('time', inplace=True, drop=True)

    feature_df = add_future_price(feature_df, n_steps_ahead=6)

    print(feature_df)


if __name__ == "__main__":
    main()