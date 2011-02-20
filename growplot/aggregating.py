
def create_aggregator(name):
    factory_name = name.capitalize() + "Aggregator"
    return globals()[factory_name]()


class NoneAggregator:
    def aggregate(self, value):
        return value


class SumAggregator:
    def __init__(self):
        self.sum = 0

    def aggregate(self, value):
        self.sum += value
        return self.sum


class AvgAggregator:
    def __init__(self):
        self.sum = 0
        self.count = 0

    def aggregate(self, value):
        self.sum += value
        self.count += 1
        return self.sum / float(self.count)

