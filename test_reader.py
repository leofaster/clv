import pytest
from datetime import datetime
from collections import defaultdict
from client_reader import Order, Storage


class TestOrder():

    def test_order_eq_ok(self):
        order = Order('order_id', 'order_item_id', 10, 78.998, '2017-09-04')
        order2 = Order('order_id', 'order_item_id', 10, 78.998, '2017-09-04')
        assert order == order2

    def test_order_eq_false(self):
        order = Order('order_id', 'order_item_id', 10, 78.998, '2017-09-04')
        order2 = Order('order_id2', 'order_item_id', 10, 78.998, '2017-09-04')
        assert order != order2

    def test_bad_date(self):
        with pytest.raises(ValueError):
            Order('order_id', 'order_item_id', 10, 78.998, 'fecha')

    def test_hasable(self):
        order = Order('order_id', 'order_item_id', 10, 78.998, '2017-09-04')
        order2 = Order('order_id98765432', 'order_item_id', 10, 78.998, '2017-09-04')
        order_list = [order, order2]
        order_set = set(order_list)
        assert order in order_set
        assert order2 in order_list
        assert order in order_set
        assert order2 in order_list

    def test_bad_revenue(self):
        order = Order('order_id', 'order_item_id', 10, 'NA', '2017-09-04')
        assert order.revenue == 0

    def test_good_revenue(self):
        order = Order('order_id', 'order_item_id', 10, 1234, '2017-09-04')
        assert order.revenue == 1234

    def test_bad_items_number(self):
        order = Order('order_id', 'order_item_id', 'NA', 78.998, '2017-09-04')
        assert order.items == 0

    def test_good_items_number(self):
        order = Order('order_id', 'order_item_id', 98765, 78.998, '2017-09-04')
        assert order.items == 98765

    def test_set(self):
        order = Order(4682271, 'order_item_id', 10, 78.998, '2017-09-04')
        order2 = Order(4682271, 'order_item_id', 10, 78.998, '2017-09-04')
        list_order = [order, order2]
        set_order = set(list_order)
        assert len(list_order) == 2
        assert len(set_order) == 1


class TestStorage:

    def new_storate(self):
        today = datetime.strptime('2017-10-17', '%Y-%m-%d')
        return Storage(today)

    def test_init_date(self):
        storage = self.new_storate()
        assert storage.today == datetime.strptime('2017-10-17', '%Y-%m-%d')
        assert len(storage.storage) == 0
        assert type(storage.storage) == defaultdict

    def test_add_order(self):
        storage = self.new_storate()
        order = Order(4682267, 21357917, 1, 32.78, '2017-09-04')
        storage.add_order('client', order)
        assert len(storage.storage) == 1
        assert order in storage.storage['client']

    def test_max_items(self):
        storage = self.new_storate()
        order = Order(4682267, 21357917, 1, 32.78, '2017-09-04')
        order1 = Order(4682268, 21357917, 2, 32.78, '2017-09-04')
        order2 = Order(4682269, 21357917, 3, 32.78, '2017-09-04')
        order3 = Order(4682270, 21357917, 4, 32.78, '2017-09-04')
        order4 = Order(4682271, 21357917, 10, 32.78, '2017-09-04')
        storage.add_order('client', order)
        storage.add_order('client', order1)
        storage.add_order('client', order2)
        storage.add_order('client', order3)
        storage.add_order('client', order4)
        assert storage.get_order_max_items('client') == 10

    def test_get_order_max_reveneu(self):
        storage = self.new_storate()
        order = Order(4682267, 21357917, 1, 32.78, '2017-09-04')
        order1 = Order(4682268, 21357917, 2, 90.87654, '2017-09-04')
        order2 = Order(4682269, 21357917, 3, 129, '2017-09-04')
        order3 = Order(4682270, 21357917, 4, 98, '2017-09-04')
        order4 = Order(4682271, 21357917, 10, 31, '2017-09-04')
        storage.add_order('client', order)
        storage.add_order('client', order1)
        storage.add_order('client', order2)
        storage.add_order('client', order3)
        storage.add_order('client', order4)
        assert storage.get_order_max_reveneu('client') == 129

    def test_get_order_total_revenue(self):
        storage = self.new_storate()
        order = Order(4682267, 21357917, 1, 32.78, '2017-09-04')
        order1 = Order(4682268, 21357917, 2, 32.78, '2017-09-04')
        order2 = Order(4682269, 21357917, 3, 32.78, '2017-09-04')
        order3 = Order(4682270, 21357917, 4, 32.78, '2017-09-04')
        order4 = Order(4682271, 21357917, 10, 32.78, '2017-09-04')
        storage.add_order('client', order)
        storage.add_order('client', order1)
        storage.add_order('client', order2)
        storage.add_order('client', order3)
        storage.add_order('client', order4)
        assert storage.get_order_total_revenue('client') == 163.9

    def test_get_orders_number(self):
        storage = self.new_storate()
        order = Order(4682267, 21357917, 1, 32.78, '2017-09-04')
        order1 = Order(4682267, 21357917, 2, 32.78, '2017-09-04')
        order2 = Order(4682267, 21357917, 3, 32.78, '2017-09-04')
        order3 = Order(4682, 21357917, 4, 32.78, '2017-09-04')
        order4 = Order(4682267, 21357917, 10, 32.78, '2017-09-04')
        storage.add_order('client', order)
        storage.add_order('client', order1)
        storage.add_order('client', order2)
        storage.add_order('client', order3)
        storage.add_order('client', order4)
        assert storage.get_orders_number('client') == 2

    def test_get_days_since_last_order(self):
        storage = self.new_storate()
        order = Order(4682261, 21357917, 1, 32.78, '2017-10-10')
        order1 = Order(4682262, 21357917, 2, 32.78, '2017-10-02')
        order2 = Order(4682263, 21357917, 3, 32.78, '2017-07-17')
        order3 = Order(4683342, 21357917, 4, 32.78, '2017-08-17')
        order4 = Order(4682327, 21357917, 10, 32.78, '2017-09-17')
        storage.add_order('client', order)
        storage.add_order('client', order1)
        storage.add_order('client', order2)
        storage.add_order('client', order3)
        storage.add_order('client', order4)
        assert storage.get_days_since_last_order('client') == 7

    def test_calculate_max_interval(self):
        storage = self.new_storate()
        order = Order(4682261, 21357917, 1, 32.78, '2017-12-30')
        order1 = Order(4682262, 21357917, 2, 32.78, '2017-10-02')
        order2 = Order(4682263, 21357917, 3, 32.78, '2017-07-17')
        order3 = Order(4683342, 21357917, 4, 32.78, '2017-08-17')
        order4 = Order(4682327, 21357917, 10, 32.78, '2017-09-17')
        orders = [order, order1, order2, order3, order4]
        assert storage.calculate_max_interval(orders) == 89

    def test_calculate_avg_longest_interval(self):
        storage = self.new_storate()

        order = Order(4682261, 21357917, 1, 32.78, '2017-10-30')
        order1 = Order(4682262, 21357917, 2, 32.78, '2017-10-15')
        storage.add_order('client', order)
        storage.add_order('client', order1)

        order2 = Order(4682263, 21357917, 3, 32.78, '2017-07-17')
        order3 = Order(4683342, 21357917, 4, 32.78, '2017-07-21')
        storage.add_order('client1', order2)
        storage.add_order('client1', order3)

        assert not hasattr(storage, 'avg_interval')
        storage.calculate_avg_longest_interval()
        assert storage.avg_interval == 9.5

    def test_get_longest_interval_between_two_consecutive_orders(self):
        storage = self.new_storate()

        order = Order(4682261, 21357917, 1, 32.78, '2017-09-30')
        order1 = Order(4682262, 21357917, 2, 32.78, '2017-09-15')
        storage.add_order('client', order)
        storage.add_order('client', order1)

        order2 = Order(4682263, 21357917, 3, 32.78, '2017-07-17')
        order3 = Order(4683342, 21357917, 4, 32.78, '2017-07-21')
        storage.add_order('client1', order2)
        storage.add_order('client1', order3)

        order4 = Order(4682327, 21357917, 10, 32.78, '2017-10-06')
        storage.add_order('client2', order4)

        assert not hasattr(storage, 'avg_interval')
        storage.calculate_avg_longest_interval()
        assert storage.get_longest_interval_between_two_consecutive_orders('client') == 15
        assert storage.get_longest_interval_between_two_consecutive_orders('client1') == 4
        assert storage.get_longest_interval_between_two_consecutive_orders('client2') == 20.5
