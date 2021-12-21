class Counter:
    '''Klasse zum Zählen der Vorkommnisse eines Ereignisses'''
    def __init__(self, name, sup_counter = None):
        self.name = name
        self.sup_counter = sup_counter
        self.output_writer = None
        self.value = 0

    def reset(self):
        self.value = 0

    def increment(self):
        self.value += 1
        if self.sup_counter is not None:
            self.sup_counter.increment()
        if self.output_writer is not None:
            self.output_writer.update()

    def set(self, new_value):
        diff = new_value - self.value
        self.value = new_value
        if self.sup_counter is not None:
            self.sup_counter.set(self.sup_counter.value + diff)
        if self.output_writer is not None:
            self.output_writer.update()

    def __str__(self):
        return "counter{:<21} {}".format("("+self.name+"):", self.value)
