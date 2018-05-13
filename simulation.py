import random

import communications
import geometry

class SimulatedServerConnection(object):
    """I simulate a communications with a server"""
    def receive_updates(self):
        return [
            communications.RectangleUpdate(
                geometry.Cartesian(
                    640 * random.random(),
                    480 * random.random()
                ),
                (255 * random.random(),
                 255 * random.random(),
                 255 * random.random())
            )
        ]

    def send_events(self, _):
        pass
