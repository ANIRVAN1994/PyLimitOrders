from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, buy: bool, product_id: str, amount: float, limit: float) -> None:
        """
        Adds a limit order to the agent.

        :param buy: True if the order is to buy, False if the order is to sell
        :param product_id: The product ID for the order
        :param amount: The amount to buy or sell
        :param limit: The limit price for the order
        """
        order = {
            'buy': buy,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float) -> None:
        """
        Called when there is a price tick for a product.

        :param product_id: The ID of the product
        :param price: The current price of the product
        """
        # Check if there are any orders that can be executed at the current price
        for order in self.orders[:]:
            if order['product_id'] == product_id:
                if order['buy'] and price <= order['limit']:
                    # Execute buy order
                    self.execution_client.buy(product_id, order['amount'])
                    self.orders.remove(order)
                elif not order['buy'] and price >= order['limit']:
                    # Execute sell order
                    self.execution_client.sell(product_id, order['amount'])
                    self.orders.remove(order)
