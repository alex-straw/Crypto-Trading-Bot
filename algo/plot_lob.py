import matplotlib.pyplot as plt
import numpy as np


# def plot_limit_order_book(lob_dict):
#     """ Plots a limit order book """
#     fig, ax = plt.subplots()
#     ax.plot(lob_dict['ask_prices'], lob_dict['ask_cum_qtys'], label='asks', color='red')
#     ax.plot(lob_dict['bid_prices'], lob_dict['bid_cum_qtys'], label='bids', color='green')
#
#     plt.fill_between(lob_dict['ask_prices'], lob_dict['ask_cum_qtys'], color='red', alpha=0.3)
#     plt.fill_between(lob_dict['bid_prices'], lob_dict['bid_cum_qtys'], color='green', alpha=0.3)
#
#     ax.set_xlim(lob_dict['bid_prices'][-1], lob_dict['ask_prices'][-1])
#     ax.set_ylim(bottom=0)
#     ax.grid()
#     ax.legend()
#     plt.title('Limit Order Book Plot')
#     ax.set_xlabel('Normalised Price (Divided by Market Price)')    ax.set_ylabel('Normalised Quantity')
#
#     plt.show()


def plot_feature_lob(feature_dict):
    """ Plots a limit order book """
    fig, ax = plt.subplots()
    ax.plot(feature_dict['bid'], feature_dict['bid_qtys'], label='bids', color='green')
    ax.plot(feature_dict['ask'], feature_dict['ask_qtys'], label='asks', color='red')

    plt.fill_between(feature_dict['bid'], feature_dict['bid_qtys'],  color='green', alpha=0.3)
    plt.fill_between(feature_dict['ask'], feature_dict['ask_qtys'], color='red', alpha=0.3)

    ax.set_ylim(bottom=0)
    ax.grid()
    ax.legend()
    plt.title('Limit Order Book Plot')
    ax.set_xlabel('Normalised Price (Divided by Market Price)')
    ax.set_ylabel('Normalised Quantity')
    plt.show()