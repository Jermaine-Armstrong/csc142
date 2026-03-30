class Vehicle:
    def __init__(self, name, fuel_capacity, cost_per_gallon, miles_per_gallon):
        self._name = name
        self._fuel_capacity = fuel_capacity
        self._cost_per_gallon = cost_per_gallon
        self._miles_per_gallon = miles_per_gallon

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def fuel_capacity(self):
        return self._fuel_capacity

    @fuel_capacity.setter
    def fuel_capacity(self, value):
        self._fuel_capacity = value

    @property
    def cost_per_gallon(self):
        return self._cost_per_gallon

    @cost_per_gallon.setter
    def cost_per_gallon(self, value):
        self._cost_per_gallon = value

    @property
    def miles_per_gallon(self):
        return self._miles_per_gallon

    @miles_per_gallon.setter
    def miles_per_gallon(self, value):
        self._miles_per_gallon = value

    @property
    def range(self):
        return self._fuel_capacity * self._miles_per_gallon

    @property
    def cost_per_mile(self):
        return self._cost_per_gallon / self._miles_per_gallon


vehicles = [
    Vehicle('Car', 12, 4.2, 28),
    Vehicle('Motorcycle', 4, 4.2, 55),
    Vehicle('Bus', 100, 4.0, 6),
    Vehicle('Train', 3000, 3.5, 0.8),
    Vehicle('Plane', 5000, 5.8, 0.2)
]

vehicles.sort(key=lambda v: v.cost_per_mile)

print(f"{'Name':<12} {'Range':>10} {'Cost/Mile':>12}")
for v in vehicles:
    print(f"{v.name:<12} {v.range:>10.1f} {v.cost_per_mile:>12.3f}")
