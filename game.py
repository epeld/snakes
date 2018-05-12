
class Game(object):
    def __init__(self):
        self.done = False

    def set_done(self, done=True):
        self.done = done

    def get_done(self):
        return self.done
