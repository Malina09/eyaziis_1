class MetricCalculator:
    def __init__(self):
        self.a = 20
        self.b = 1
        self.c = 2
        self.d = 10

        self.recall = self.calculate_recall()
        self.precision = self.calculate_precision()
        self.accuracy = self.calculate_accuracy()
        self.error = self.calculate_error()
        self.f_measure = self.calculate_fmeasure()

    def calculate_recall(self):
        return self.a / (self.a + self.c)

    def calculate_precision(self):
        return self.a / (self.a + self.b)

    def calculate_accuracy(self):
        return (self.a + self.d) / (self.a + self.b + self.c + self.d)

    def calculate_error(self):
        return (self.b + self.c) / (self.a + self.b + self.c + self.d)

    def calculate_fmeasure(self):
        if self.precision == 0 or self.recall == 0:
            return 0
        elif self.precision == self.recall:
            return self.precision
        else:
            return 2 / (self.precision ** -1 + self.recall ** -1)
