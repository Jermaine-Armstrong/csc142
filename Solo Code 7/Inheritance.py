from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def calculate_cost(self):
        pass


class ByWeightItem(Item):
    def __init__(self, name, weight, cost_per_pound):
        super().__init__(name)
        self._weight = weight
        self._cost_per_pound = cost_per_pound

    @property
    def weight(self):
        return self._weight

    @property
    def cost_per_pound(self):
        return self._cost_per_pound

    def calculate_cost(self):
        return self._weight * self._cost_per_pound


class ByQuantityItem(Item):
    def __init__(self, name, quantity, cost_each):
        super().__init__(name)
        self._quantity = quantity
        self._cost_each = cost_each

    @property
    def quantity(self):
        return self._quantity

    @property
    def cost_each(self):
        return self._cost_each

    def calculate_cost(self):
        return self._quantity * self._cost_each


class Grapes(ByWeightItem):
    def __init__(self, weight):
        super().__init__('Grapes', weight, 2.99)


class Bananas(ByWeightItem):
    def __init__(self, weight):
        super().__init__('Bananas', weight, 0.69)


class Oranges(ByQuantityItem):
    def __init__(self, quantity):
        super().__init__('Oranges', quantity, 0.79)


class Cantaloupes(ByQuantityItem):
    def __init__(self, quantity):
        super().__init__('Cantaloupes', quantity, 3.49)


class Order:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def calculate_total(self):
        total = 0
        for item in self._items:
            total += item.calculate_cost()
        return total

    def get_items(self):
        return self._items

    def __len__(self):
        return len(self._items)


order = Order()
order.add_item(Grapes(1.5))
order.add_item(Bananas(2.2))
order.add_item(Oranges(6))
order.add_item(Cantaloupes(2))

print('Receipt')
print('--------')
for item in order.get_items():
    print(f"{item.name}: ${item.calculate_cost():.2f}")
print('--------')
print(f"Items: {len(order)}")
print(f"Total: ${order.calculate_total():.2f}")
