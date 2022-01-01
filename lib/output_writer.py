import json

import lib.settings as se
from lib.timer import Timer

class Output_Writer:
    '''Klasse zum Schreiben von Zählern in eine Ausgabedatei'''
    def __init__(self, counters):
        self.counters = counters
        for counter in self.counters:
            counter.output_writer = self
        # Pfad der Ausgabedatei
        self.file_path = se.OUTPUT_FILE_PATH
        # Timer zum messen der Zeit seit dem letzten Aufruf von write()
        self.timer = Timer("last_write")
        self.write()

    # es wird höchstens alle 5 Sekunden geupdated
    # so wird die json Datei nicht zu oft überschrieben
    def update(self):
        if self.timer.eval() >= 10:
            self.write()     

    # schreibe die Werte der Zähler unter ihren Namen in die Ausgabedatei
    def write(self):
        with open(self.file_path, "w") as f:
            json.dump({counter.name : counter.get_value() for counter in self.counters} , f, indent=4, sort_keys=True)
        self.timer.reset()
        self.timer.begin()