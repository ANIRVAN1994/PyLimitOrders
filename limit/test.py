import unittest
from unittest.mock import MagicMock
from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from limit.limit_order_agent import LimitOrderAgent

class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        self.mock_execution_client = MagicMock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_add_order(self):
        self.agent.add_order(buy=True, product_id="product_1", amount=10, limit=100)
        self.agent.add_order(buy=False, product_id="product_2", amount=5, limit=150)
        self.assertEqual(len(self.agent.orders), 2)
        self.assertEqual(self.agent.orders[0], {'buy': True, 'product_id': 'product_1', 'amount': 10, 'limit': 100})
        self.assertEqual(self.agent.orders[1], {'buy': False, 'product_id': 'product_2', 'amount': 5, 'limit': 150})

    def test_on_price_tick_buy_order(self):
        self.agent.add_order(buy=True, product_id="product_1", amount=10, limit=100)
        self.agent.on_price_tick(product_id="product_1", price=95)
        self.mock_execution_client.buy.assert_called_with("product_1", 10)
        self.assertEqual(len(self.agent.orders), 0)

    def test_on_price_tick_sell_order(self):
        self.agent.add_order(buy=False, product_id="product_1", amount=10, limit=100)
        self.agent.on_price_tick(product_id="product_1", price=105)
        self.mock_execution_client.sell.assert_called_with("product_1", 10)
        self.assertEqual(len(self.agent.orders), 0)

    def test_on_price_tick_no_execution(self):
        self.agent.add_order(buy=True, product_id="product_1", amount=10, limit=100)
        self.agent.on_price_tick(product_id="product_1", price=105)
        self.mock_execution_client.buy.assert_not_called()
        self.assertEqual(len(self.agent.orders), 1)

        self.agent.add_order(buy=False, product_id="product_1", amount=10, limit=100)
        self.agent.on_price_tick(product_id="product_1", price=95)
        self.mock_execution_client.sell.assert_not_called()
        self.assertEqual(len(self.agent.orders), 2)

if __name__ == '__main__':
    unittest.main()
