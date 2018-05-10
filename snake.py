
class SpatialCommit(object):
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading

    def get_position(self):
        return self.position

    def get_heading(self):
        return self.heading


class CommitHistory(object):
    def __init__(self, commits=[]):
        self.commits = commits

    def commit(self, item):
        self.commits.append(item)

    def commit_all(self, items):
        self.commits.extend(items)

    def get_commits(self):
        return self.commits

    def clear_commits(self):
        self.commits.clear()

#
# Snake States
#
class SnakeGoingStraight(object):
    def update_heading(self, heading):
        return heading

class SnakeTurningLeft(object):
    def update_heading(self, heading, time_delta):
        heading.angle -= SNAKE_TURN_SPEED * time_delta;

class SnakeTurningRight(object):
    def update_heading(self, heading, time_delta):
        heading.angle += SNAKE_TURN_SPEED * time_delta;

GOING_STRAIGHT = SnakeGoingStraight()
TURNING_LEFT = SnakeTurningLeft()
TURNING_Right = SnakeTurningRight()

#
# Snake Object
#
class Snake(object):
    def __init__(self, position, heading, state=GOING_STRAIGHT):
        self.history = CommitHistory()
        self.position = position
        self.heading = heading
        self.state = state

    def commit_movement(self, time_delta):
        """Move the snake forward using the given time_delta.

Adds the new spatial configuration to history"""
        self.history.commit(self.calculate_spatial_commit(time_delta))

    def rewrite_history(self, commits=[]):
        "Remove all commits from the timeline, add the supplied list instead"
        self.history.clear_commits()
        self.history.commit_all(commits)

    def commits_synchronized(self):
        "Notify this instance that all its commits have been synchronized with the server"
        self.position = self.calculate_position()
        self.heading = self.calculate_heading()
        self.history.clear_commits()

    def calculate_heading(self):
        if self.history.is_empty():
            return self.heading
        return self.history.get_commits[-1].get_heading()

    def calculate_position(self):
        if self.history.is_empty():
            return self.position
        return self.history.get_commits[-1].get_position()

    def calculate_spatial_commit(self, time_delta):
        heading = self.calculate_heading()
        position = self.calculate_position()
        commit = SpatialCommit(position + heading * time_delta,
                               self.state.update_heading(heading, time_delta))

    def get_last_synchronized_position(self):
        return self.position

    def get_last_synchronized_heading(self):
        return self.heading
