import pandas as pd
import cbpro_api
import plot_lob
import numpy as np


def clean_lob(_lob, middle_pct):

    def get_sub_array_items(array, position):
        return [float(sub_array[position]) for sub_array in array]

    def get_cumsum(array):
        return np.cumsum(array)

    def estimate_fair_price(asks, bids):
        """ Estimates the fair price by finding the middle of the bid-ask spread """
        return 0.5 * (asks[0] + bids[0])

    def central_data(_lob, middle_pct, market_price):
        asks_cutoff_idx = next(x for x, val in enumerate(cleaned_lob['asks_prices']) if val > market_price*(1+middle_pct/2))
        bids_cutoff_idx = next(x for x, val in enumerate(cleaned_lob['bids_prices']) if val < market_price*(1-middle_pct/2))

        cleaned_lob['asks_prices'] = cleaned_lob['asks_prices'][0:asks_cutoff_idx]
        cleaned_lob['asks_cumsum_qtys'] = cleaned_lob['asks_cumsum_qtys'][0:asks_cutoff_idx]

        cleaned_lob['bids_prices'] = cleaned_lob['bids_prices'][0:bids_cutoff_idx]
        cleaned_lob['bids_cumsum_qtys'] = cleaned_lob['bids_cumsum_qtys'][0:bids_cutoff_idx]

        return cleaned_lob

    def normalise_lob_qtys(cleaned_lob):
        """ Divide cumulative quantities by the sum of all quantities - like a PDF """

        total_qty = sum(cleaned_lob['asks_cumsum_qtys']) + sum(cleaned_lob['bids_cumsum_qtys'])

        cleaned_lob['asks_cumsum_qtys'] = cleaned_lob['asks_cumsum_qtys'] / total_qty
        cleaned_lob['bids_cumsum_qtys'] = cleaned_lob['bids_cumsum_qtys'] / total_qty

        return cleaned_lob

    def normalise_prices(cleaned_lob, market_price):
        cleaned_lob['asks_prices'] = [x/market_price for x in cleaned_lob['asks_prices']]
        cleaned_lob['bids_prices'] = [x/market_price for x in cleaned_lob['bids_prices']]
        return cleaned_lob

    cleaned_lob = {
        'asks_prices': get_sub_array_items(_lob['asks'], position=0),
        'asks_cumsum_qtys': get_cumsum(get_sub_array_items(_lob['asks'], position=1)),
        'bids_prices': get_sub_array_items(_lob['bids'], position=0),
        'bids_cumsum_qtys': get_cumsum(get_sub_array_items(_lob['asks'], position=1))
    }

    market_price = estimate_fair_price(cleaned_lob['asks_prices'], cleaned_lob['bids_prices'])

    cleaned_lob = central_data(cleaned_lob, middle_pct, market_price)
    cleaned_lob = normalise_lob_qtys(cleaned_lob)
    cleaned_lob = normalise_prices(cleaned_lob, market_price)

    return cleaned_lob, market_price


def get_curve_features(cleaned_lob, n_points_per_curve, middle_pct):

    bids_bins = np.linspace(1-(middle_pct/2), 1, n_points_per_curve)
    asks_bins = np.linspace(1+(middle_pct/2), 1, n_points_per_curve)

    bids_digitised = np.digitize(cleaned_lob['bids_prices'], bids_bins)
    asks_digitised = np.digitize(cleaned_lob['asks_prices'], asks_bins)

    def get_bin_counts(digitised_array):
        unique, counts = np.unique(digitised_array, return_counts=True)
        return dict(zip(unique, counts))

    def get_indexes_from_counts(bin_counts):
        for key in bin_counts:
            if key != 1:
                bin_counts[key] += bin_counts[key-1]
        return bin_counts

    def get_bin_indexes(digitised_bins):
        bin_count_dict = get_bin_counts(digitised_bins)
        return get_indexes_from_counts(bin_count_dict)

    def get_quantity_by_bin(qty_vect, count_by_bin, bins):
        qty_by_bin = {}
        for key in count_by_bin:
            qty_by_bin[bins[key]] = qty_vect[count_by_bin[key]]
        return qty_by_bin

    bid_bin_edges = get_bin_indexes(bids_digitised)
    ask_bin_edges = get_bin_indexes(asks_digitised)

    bid_features = get_quantity_by_bin(cleaned_lob['bids_cumsum_qtys'], bid_bin_edges, bids_bins)
    ask_features = get_quantity_by_bin(cleaned_lob['asks_cumsum_qtys'], ask_bin_edges, asks_bins)

    print(ask_features)
    print(bid_features)


def main():

    api_request = {
        'product': 'BTC-USD',
        'level': 2
    }

    middle_pct = 0.1
    n_points_per_curve = 9

    lob = cbpro_api.get_lob(api_request['product'], api_request['level'])
    cleaned_lob, market_price = clean_lob(lob, middle_pct)

    plot_lob.plot_limit_order_book(cleaned_lob)

    get_curve_features(cleaned_lob, n_points_per_curve, middle_pct)

    # feature_dict[market_price] = market_price

    # print(feature_dict)


if __name__ == "__main__":
    main()
