class Counter:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def reset(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def __str__(self):
        return "counter{:<21} {}".format("("+self.name+"):", self.value)
