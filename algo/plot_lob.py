import matplotlib.pyplot as plt
import numpy as np


def plot_limit_order_book(lob_dict):
    """ Plots a limit order book """
    fig, ax = plt.subplots()
    ax.plot(lob_dict['asks_prices'], lob_dict['asks_cumsum_qtys'], label='asks', color='red')
    ax.plot(lob_dict['bids_prices'], lob_dict['bids_cumsum_qtys'], label='bids', color='green')

    plt.fill_between(lob_dict['asks_prices'], lob_dict['asks_cumsum_qtys'], color='red', alpha=0.3)
    plt.fill_between(lob_dict['bids_prices'], lob_dict['bids_cumsum_qtys'], color='green', alpha=0.3)


    ax.grid()
    ax.legend()
    plt.title('Limit Order Book Plot')
    ax.set_xlabel('Normalised Price (Divided by Market Price)')
    ax.set_ylabel('Normalised Quantity')
    plt.show()