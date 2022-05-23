import matplotlib.pyplot as plt
import numpy as np


def plot_limit_order_book(lob_dict):
    """ Plots a limit order book """
    fig, ax = plt.subplots()
    ax.plot(lob_dict['asks_prices'], lob_dict['asks_cumsum_qtys'], label='asks')
    ax.plot(lob_dict['bids_prices'], lob_dict['bids_cumsum_qtys'], label='bids')
    ax.grid()
    ax.legend()
    plt.title('Limit Order Book Plot')
    ax.set_xlabel('Price ($)')
    ax.set_ylabel('Normalised Quantity')
    plt.show()