import csv
from datetime import datetime
from collections import defaultdict

import dill
import numpy

from server import db, User


class Order:

    def __init__(
        self, order_id, order_item_id, num_items, revenue, created_at_date
    ):
        self.id = order_id
        self.item_id = order_item_id
        try:
            self.items = int(num_items)
        except ValueError as e:
            self.items = 0
        try:
            self.revenue = float(revenue)
        except ValueError as e:
            self.revenue = 0
        try:
            self.created = datetime.strptime(created_at_date, '%Y-%m-%d')
        except ValueError as e:
            print(e)
            raise

    def __eq__(self, other):
        return (self.id, self.created) == other

    def __hash__(self):
        return hash((self.id, self.created))

    def __str__(self):
        return 'Order(%s)' % str(self.id)

    def __repr__(self):
        return 'Order(%s)' % self.id


class Storage:

    def __init__(self, today):
        self.today = today
        self.storage = defaultdict(list)

    def add_order(self, customer_id, order):
        self.storage[customer_id].append(order)

    def get_order_max_items(self, customer_id):
        '''
        return the higher number of items that any order has from the same
        customer
        '''
        return max([order.items for order in self.storage[customer_id]])

    def get_order_max_reveneu(self, customer_id):
        '''
        return the order with the max revenue
        '''
        return max([order.revenue for order in self.storage[customer_id]])

    def get_order_total_revenue(self, customer_id):
        '''
        return the sum of every order that the client has
        '''
        return sum([order.revenue for order in self.storage[customer_id]])

    def get_orders_number(self, customer_id):
        '''
        return the number of orders that the customer_id has
        '''
        return len(set(self.storage[customer_id]))

    def get_days_since_last_order(self, customer_id):
        '''
        returns the number of days between "today" and the last order that the
        client did.
        '''
        older_order = max(
            self.storage[customer_id], key=lambda order: order.created
        )
        return (self.today - older_order.created).days

    def get_longest_interval_between_two_consecutive_orders(self, customer_id):
        '''
        wrapper function.
        '''
        if len(self.storage[customer_id]) < 2:
            return (
                self.avg_interval + self.get_days_since_last_order(customer_id)
            )
        else:
            return self.calculate_max_interval(self.storage[customer_id])

    def calculate_avg_longest_interval(self):
        '''
        sets on the class the avg longest internval between every customer
        that has more than 1 order in his log.
        '''
        intervals = []
        for client, orders in self.storage.items():
            if len(orders) > 1:
                max_interval = self.calculate_max_interval(orders)
                intervals.append(max_interval)
        self.avg_interval = sum(intervals) / len(intervals)

    def calculate_max_interval(self, orders):
        '''
        for every list of orders returns the max interval between
        two consecutive orders.
        '''
        orders_sorted = sorted(orders, key=lambda order: order.created)
        max_interval = 0
        for i, order in enumerate(orders_sorted[:-1]):
            internal_interval = (
                orders_sorted[i + 1].created - order.created).days
            if internal_interval > max_interval:
                    max_interval = internal_interval
        return max_interval

    def get_data_sorted(self):
        '''
        wrapper function to sort the function calling.
        '''
        data = []
        data_append = data.append
        for client, orders in self.storage.items():
            data_append(
                [
                    self.get_order_max_items(client),
                    self.get_order_max_reveneu(client),
                    self.get_order_total_revenue(client),
                    self.get_orders_number(client),
                    self.get_days_since_last_order(client),
                    self.get_longest_interval_between_two_consecutive_orders(
                        client
                    )
                ]
            )
        return data


def read_orders_from_file(storage, file='orders.csv'):

    with open(file, 'r+') as file:
        orders = csv.reader(file, delimiter=',')
        next(orders)  # skip the headers
        for (
            customer_id, order_id, order_item_id, num_items,
            revenue, created_at_date
        ) in orders:
            storage.add_order(
                customer_id,
                Order(
                    order_id, order_item_id, num_items, revenue, created_at_date
                )
            )


def calculate_predictions(data, clients, model='model.dill'):
    with open(model, 'rb') as model_file:
        model = dill.load(model_file)
        numpy_array = numpy.array(data)
        return model.predict(numpy_array)


def write_to_file(clients, predictions, output='exit.csv'):
    with open(output, 'w+', newline='') as csvfile:
        fieldnames = ['customer_id', 'predicted_clv']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, client in enumerate(clients):
            writer.writerow(
                {
                    'customer_id': client,
                    'predicted_clv': predictions[i]
                }
            )


def get_data():
    '''
    wrapper function to give the calling order.
    returns the list of clients and the list of predictions
    '''
    today = datetime.strptime('2017-10-17', '%Y-%m-%d')
    storage = Storage(today)
    read_orders_from_file(storage)
    storage.calculate_avg_longest_interval()
    data = storage.get_data_sorted()
    clients = storage.storage.keys()
    predictions = calculate_predictions(data, clients)
    return clients, predictions


def create_db():
    db.create_all()


def fill_database(clients, predictions):
    '''
    fill the database that Flask will use.
    '''
    for i, client in enumerate(clients):
        user = User(id=client, clv=predictions[i])
        db.session.add(user)
    db.session.commit()


def main():
    clients, predictions = get_data()
    create_db()
    write_to_file(clients, predictions)
    fill_database(clients, predictions)


if __name__ == '__main__':
    main()
