import cbpro_api
import bisect_lob
import numpy as np
import plot_lob
import time
import pandas as pd
import sys


def get_market_price(lob):
    """ Midpoint of bid-ask spread """
    best_ask = float(lob['asks'][0][0])
    best_bid = float(lob['bids'][0][0])
    return (best_bid + best_ask) / 2


def get_lob_data_dict(lob):
    """
    Original format for lob is many arrays: [[Price_1, Qty_1, Type],...,[Price_n, Qty_n, Type_n]]

    This function uses list comprehensions to extract arrays of prices and quantities to make data manipulation
    easier
    """

    def get_array(lob, side, position):
        return [float(sub_array[position]) for sub_array in lob[side]]

    lob_dict = {
        'bid_prices': get_array(lob, 'bids', position=0),
        'ask_prices': get_array(lob, 'asks', position=0),
        'bid_qtys': get_array(lob, 'bids', position=1),
        'ask_qtys': get_array(lob, 'bids', position=1)
    }

    return lob_dict


def normalise_prices(lob_dict, market_price):
    """ Normalise prices around the market price """
    for order_type in ['bid', 'ask']:
        lob_dict[f'{order_type}_prices'] = [price / market_price for price in lob_dict[f'{order_type}_prices']]

    return lob_dict


def add_cumsum_qtys(lob_dict):
    """ Adds normalised cumulative quantities to the LOB dictionary """

    for order_type in ['bid', 'ask']:
        lob_dict[f'{order_type}_cum_qtys'] = np.cumsum(lob_dict[f'{order_type}_qtys'])

    return lob_dict


def get_lob_features(lob_dict, lob_price_depth_percentage, num_points_per_side):
    """
    Generates a linear set of points from the normalised market price : 1, to a certain percentage above
    and below. In this case, 5% above and 5% below. The LOB is bisected up and down to find the closest index
    to the associated normalised price. The corresponding cumulative normalised quantity is then found using
    that index and stored in the points of interest array. This allows
    """

    points_of_interest = {
        'bid': np.linspace(1, 1 - lob_price_depth_percentage, num_points_per_side),
        'ask': np.linspace(1, 1 + lob_price_depth_percentage, num_points_per_side),
        'bid_qtys': [],
        'ask_qtys': []
    }

    for price in points_of_interest['ask']:
        idx = bisect_lob.find_closest_index(lob_dict['ask_prices'], price)
        points_of_interest['ask_qtys'].append(lob_dict['ask_cum_qtys'][idx])

    for price in points_of_interest['bid']:
        idx = bisect_lob.find_closest_index_rev(lob_dict['bid_prices'], price)
        points_of_interest['bid_qtys'].append(lob_dict['bid_cum_qtys'][idx])

    return points_of_interest


def format_features_for_data_frame(lob_points_of_interest, market_price, call_time):
    """
    Adds a key for each different linearly spaced bid/ask point and its respective quantity.
    Market price and call_time have also been added for labelling purposes.
    """
    formatted_dict = {}

    for order_type in ['bid', 'ask']:
        for feature_idx in range(len(lob_points_of_interest[order_type])):
            normalised_price = lob_points_of_interest[order_type][feature_idx]
            quantity = lob_points_of_interest[f'{order_type}_qtys'][feature_idx]
            formatted_dict[f'{order_type}_{normalised_price}'] = quantity

    formatted_dict['market_price'] = market_price
    formatted_dict['time'] = call_time

    return formatted_dict


def retrieve_market_data(api_request, depth_percentage, feature_points_per_side):
    call_time = time.time()
    lob = cbpro_api.get_lob(api_request['product'], api_request['level'])

    if not lob:
        return False

    market_price = get_market_price(lob)

    lob_dict = get_lob_data_dict(lob)

    lob_dict = normalise_prices(lob_dict, market_price)
    lob_dict = add_cumsum_qtys(lob_dict)

    lob_points_of_interest = get_lob_features(lob_dict, depth_percentage, feature_points_per_side)
    formatted_dict = format_features_for_data_frame(lob_points_of_interest, market_price, call_time)

    # plot_lob.plot_feature_lob(lob_points_of_interest)

    return formatted_dict


def gather_data(parameters):

    api_request = {
        'product': parameters['product'],
        'level': parameters['lob_level']
    }

    collected_lob_data = pd.DataFrame()
    start_time = time.time()

    for request in range(1, parameters['n_api_calls']+1):

        formatted_dict = retrieve_market_data(
            api_request,
            parameters['lob_price_depth_percentage'],
            parameters['num_points_per_side'])

        if not formatted_dict:
            collected_lob_data.to_csv('output_data/{product}_connection_fail_data.csv'.format(product=parameters['product']))
            sys.exit("Cannot retrieve data from Coinbase Pro API. Collected data has been saved.")

        collected_lob_data = collected_lob_data.append(formatted_dict, ignore_index=True)

        print('{request} / {n}'.format(request=request, n=parameters['n_api_calls']))
        time.sleep(parameters['api_call_interval'] - ((time.time() - start_time) % parameters['api_call_interval']))

    collected_lob_data.to_csv('output_data/{product}_data.csv'.format(product=parameters['product']))


def main():

    parameters = {
        'product': 'BTC-USD',
        'lob_level': 2,
        'lob_price_depth_percentage': 0.1,
        'num_points_per_side': 20,
        'api_call_interval': 5,
        'n_api_calls': 1000
    }

    gather_data(parameters)


if __name__ == "__main__":
    main()
