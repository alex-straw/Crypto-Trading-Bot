import cbpro_api
import bisect_lob
import numpy as np
import plot_lob


def get_market_price(lob):
    """ Midpoint of bid-ask spread """
    best_ask = float(lob['asks'][0][0])
    best_bid = float(lob['bids'][0][0])
    return (best_bid+best_ask)/2


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
        lob_dict[f'{order_type}_prices'] = [price/market_price for price in lob_dict[f'{order_type}_prices']]

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
        'bid': np.linspace(1, 1-lob_price_depth_percentage, num_points_per_side),
        'ask': np.linspace(1, 1+lob_price_depth_percentage, num_points_per_side),
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


def main():
    api_request = {
        'product': 'BTC-USD',
        'level': 2
    }

    # Want to define the shape of the LOB using discretely spaced points
    # Issue: LOB doesn't have discrete bins

    # Estimate how far to go up / down
    # First handle asks as these are increasing

    lob = cbpro_api.get_lob(api_request['product'], api_request['level'])
    market_price = get_market_price(lob)

    lob_price_depth_percentage = 0.1
    num_points_per_side = 20

    lob_dict = get_lob_data_dict(lob)

    lob_dict = normalise_prices(lob_dict, market_price)
    lob_dict = add_cumsum_qtys(lob_dict)

    lob_points_of_interest = get_lob_features(lob_dict, lob_price_depth_percentage, num_points_per_side)

    # Now going to get indexes for 5% above and 5% below.
    # Begin with asks

    # ask_features = get_lob_features(lob_dict, market_price, lob_price_depth_percentage)

    plot_lob.plot_limit_order_book(lob_dict)

if __name__ == "__main__":
    main()
