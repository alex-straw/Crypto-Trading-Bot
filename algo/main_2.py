import cbpro_api


def main():
    api_request = {
        'product': 'BTC-USD',
        'level': 2
    }

    lob = cbpro_api.get_lob(api_request['product'], api_request['level'])

    print(lob)


if __name__ == "__main__":
    main()
