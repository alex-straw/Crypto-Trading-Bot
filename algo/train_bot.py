import pandas as pd


def main():
    feature_df = pd.read_csv('output_data/BTC-USD_data.csv')
    feature_df = feature_df.drop(feature_df.columns[0], axis=1)  # Drop original index column
    feature_df.set_index('time', inplace=True, drop=True)


if __name__ == "__main__":
    main()