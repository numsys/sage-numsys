import time


class Timer:
    def __init__(self):
        self.start = time.time()
        self.data = {}
        self.alreadyMeasured = 0

    def measure_time(self, name=None):
        temp = time.time() - self.start
        self.start = time.time()
        if name is not None:
            self.data[name] = temp + self.alreadyMeasured

        return temp + self.alreadyMeasured

    def get_time(self):
        temp = time.time() - self.start
        return temp + self.alreadyMeasured

    def start_timer(self):
        self.start = time.time()
        self.alreadyMeasured = 0

    def pause_timer(self):
        self.alreadyMeasured = self.alreadyMeasured + time.time() - self.start

    def continue_timer(self):
        self.start = time.time()

    def measure_and_print_time(self, text):
        print(text, self.measure_time())

    def get_data(self):
        return self.data

    def clear_times(self):
        self.data = {}
