import cbpro_api
import bisect_lob
import numpy as np


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


def get_lob_features(lob, market_price, lob_price_depth_percentage):
    upper_price_thresh = market_price * (1+lob_price_depth_percentage)  # For asks
    lower_price_thresh = market_price * (1-lob_price_depth_percentage)  # For bids

    bid_points_of_interest = np.linspace()

    for order_type in ['bid','ask']:

        if ['bid']:
            pass



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

    lob_price_depth_percentage = 0.05

    lob_dict = get_lob_data_dict(lob)

    lob_dict = normalise_prices(lob_dict, market_price)

    print(lob_dict['bid_prices'])

    # Now going to get indexes for 5% above and 5% below.
    # Begin with asks

    # ask_features = get_lob_features(lob_dict, market_price, lob_price_depth_percentage)


if __name__ == "__main__":
    main()
