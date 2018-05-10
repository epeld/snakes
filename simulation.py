import random
import math

def event_milliseconds(event):
    return event[0]

def rect_event(n):
    black = (200,0,0)
    x = n * 50
    y = 250 + 30 * math.sin(n * math.pi / 5)
    w = 50
    h = 50
    return (n * 1000,x,y,w,h,black)


events = []

def setup():
    global events
    events.extend([rect_event(i) for i in range(30)][::-1])


def get_events(ms):
    global events
    r = []
    while events:
        event = events[-1]
        if event_milliseconds(event) < ms:
            events.pop()
            r.append(event)
        else:
            break
    return r
