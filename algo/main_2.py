import cbpro_api


def get_market_price(lob):
    """ Midpoint of bid-ask spread """
    best_ask = float(lob['asks'][0][0])
    best_bid = float(lob['bids'][0][0])
    return (best_bid+best_ask)/2


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
    upper_price_thresh = market_price * (1+lob_price_depth_percentage)  # For asks
    lower_price_thresh = market_price * (1-lob_price_depth_percentage)  # For bids

    upper_price = market_price


    print(market_price)


if __name__ == "__main__":
    main()
