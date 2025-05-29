# from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple("Customer", "name fidelity")


class LineItme:
    def __init__(self, product, quantity, price) -> None:
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.quantity * self.price


class Order:
    def __init__(self, customer, cart1, promotion=None) -> None:
        self.customer = customer
        self.cart = list(cart1)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, "__total"):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self) -> str:
        return "<Order total: {:.2f} due: {:.2f}>".format(self.total(), self.due())


def FidelityPromo(order):
    if 500 <= order.customer.fidelity < 1000:
        return order.total() * 0.01
    if order.customer.fidelity >= 1000:
        return order.total() * 0.05

def BulkItemPromo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 10:
            discount += item.total() * .1
    return discount


def LargeOrderPromo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 4:
        return order.total() * 0.07
    return 0


if __name__ == "__main__":
    joe = Customer("John Doe", 500)
    ann = Customer("Ann Smith", 1500)
    cart = [LineItme("banana", 4, 0.5), LineItme("apple", 10, 1.5), LineItme("mongo", 8, 2.5), LineItme("watermellon", 5, 5.0)]
    print(Order(ann, cart, FidelityPromo))
    print(Order(ann, cart, BulkItemPromo))
    print(Order(ann, cart, LargeOrderPromo))
    print(Order(joe, cart, FidelityPromo))

    print("Hello World")
