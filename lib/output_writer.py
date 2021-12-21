import json

import lib.settings as se
from lib.timer import Timer

class Output_Writer:
    def __init__(self, counters):
        self.counters = counters
        for counter in self.counters:
            counter.output_writer = self
        self.file_path = se.OUTPUT_FILE_PATH
        self.t = Timer("abs")
        self.t.begin()
        self.timer = Timer("last_write")
        self.write()

    def update(self):
        if self.timer.eval() >= 10:
            self.write()
        


    def write(self):
        with open(self.file_path, "w") as f:
            json.dump({counter.name : counter.value for counter in self.counters} , f, indent=4, sort_keys=True)
        self.timer.reset()
        self.timer.begin()