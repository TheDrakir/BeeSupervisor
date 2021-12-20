from time import perf_counter

class Timer:
    '''Klasse zum messen des Zeitaufwands eines Vorgangs'''

    def __init__(self, name):
        self.time = 0
        self.name = name
        self.call_count = 0

    # starte den Timer
    def begin(self):
        self.time -= perf_counter()
        self.call_count += 1

    # stoppe den Timer
    def end(self):
        self.time += perf_counter()

    # gibt den String zurück, der den Namen und die Laufzeit des Timers enthält
    def __str__(self):
        return "total{:<23} {}".format("("+self.name+"):", Timer.to_time_str(self.time))

    # gibt den String zurück, der den Namen und die durchschnittliche Laufzeit des Timers enthält
    def str_avg(self):
        return "avg{:<25} {}".format("("+self.name+"):", Timer.to_time_str(self.avg()))

    # gibt die durchschnittliche Laufzeit des Timers zurück
    def avg(self):
        if not self.call_count:
            return 0
        else:
            return self.time / self.call_count

    # erstelle einen aus der Zeit t, wobei automatisch eine passende EInheit gewählt wird
    @staticmethod
    def to_time_str(t):
        if t >= 0.1:
            return str(round(t,1)) + " s"
        else:
            return str(round(1000*t,1)) + " ms"