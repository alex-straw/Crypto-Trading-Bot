import cbpro
import config


def setup_client(key, secret, passphrase):
    return cbpro.AuthenticatedClient(key, secret, passphrase)


def get_lob(product, level):
    auth_client = setup_client(config.key, config.b64secret, config.passphrase)
    lob = auth_client.get_product_order_book(product, level)
    return lob