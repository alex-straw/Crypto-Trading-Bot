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

    # Want to estimate the b

    lob = cbpro_api.get_lob(api_request['product'], api_request['level'])

    market_price = get_market_price(lob)

    print(market_price)


if __name__ == "__main__":
    main()
