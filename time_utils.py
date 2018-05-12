
class TimeConverter(object):
    """I use the equation

game_time = real_time * factor + offset

to keep track of game time"""
    def __init__(self, factor, offset=0):
        "Pass in the ratio game_time / real_time that you would like"
        self.offset = 0
        self.factor = factor

    def get_game_vs_real_ratio(self):
        return self.factor

    def calibrate(self, real_time, game_time):
        """Calibrate the offset in game time vs real_time.
Offsets occur e.g due to lag/pausing"""
        self.offset = game_time - real_time * self.factor

    def calculate_game_time(self, real_time):
        "Calculate the game_time, given a real time, using data from latest calibration"
        return self.get_offset() + real_time * factor;


class TimeTracker(object):
    "I keep track of a single point in time, and calculate deltas"
    def __init__(self, time=0):
        self.time = time

    def set_time(self, time):
        "Store a point in time"
        self.time = time

    def get_time(self):
        "Retrieve the point previously stored"
        return self.time

    def calculate_delta(self, time):
        "Calculate how much time has passed since the stored time"
        return time - self.get_time()
