"""
Room

Rooms are simple containers that has no location of their own.

"""
import random
from evennia import DefaultRoom, TICKER_HANDLER
from random import choice
from evennia import DefaultRoom
from evennia import TICKER_HANDLER
from collections import defaultdict


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass

class AmbientRoom(Room):
    """
    Here's a first pass at making a weather room.
    """
    def __init__(self):
        self.randomgoods = ["reactor-plates.",
                "high-speed graphene batteries.",
                "dogs wearing hats.",
                "weapons-grade chili.",
                "illegally-sourced tubers." ]

        self.ambient_strings = ["A forklift trundles by, carrying a huge pallet of  " + self.choice(randomgoods),
                 "A trickle of oil leaking from the ceiling-pipes splatters onto the ground nearby.",
                 "A deep, mechanical groan echoes down the length of the ship, sending shivers up the spine.",
                 "A mechanized loader rolls by on worn-down treads, hefting a pile of " + self.choice(randomgoods),
                 "Farther down the hangar, the sound of a dropped tool echoes dully against the high, metal walls."]
       

    def at_object_creation(self):
        super().at_object_creation()
        # subscribe ourselves to a ticker to repeatedly call the hook
        # "update_weather" on this object.
        self.db.interval = random.randint(5, 7)
        TICKER_HANDLER.add(
            interval=self.db.interval, callback=self.update_ambience
        )

    def update_ambience(self, *args, **kwargs):
        """
        Called by the tickerhandler at regular intervals. Even so, we
        only update 20% of the time, picking a random weather message
        when we do. The tickerhandler requires that this hook accepts
        any arguments and keyword arguments (hence the *args, **kwargs
        even though we don't actually use them in this example)
        """
        if random.random() < 0.5:
            self.msg_contents("|w%s|n" % random.choice(self.ambient_strings))



"""
class TickerRoom(DefaultRoom):
    "This room is ticked at regular intervals"

    randomgoods = ["reactor-plates.",
                "high-speed graphene batteries.",
                "dogs wearing hats.",
                "weapons-grade chili.",
                "illegally-sourced tubers." ]
    
    ECHOES = ["A forklift trundles by, carrying a huge pallet of  " + choice(randomgoods),
                 "A trickle of oil leaking from the ceiling-pipes splatters onto the ground nearby.",
                 "A deep, mechanical groan echoes down the length of the ship, sending shivers up the spine.",
                 "A mechanized loader rolls by on worn-down treads, hefting a pile of " + choice(randomgoods),
                 "Farther down the hangar, the sound of a dropped tool echoes dully against the high, metal walls."]
       
    def at_object_creation(self):
        "called only when the object is first created"
        TICKER_HANDLER.add(5, self.at_weather_update)

    def at_weather_update(self, *args, **kwargs):
        "ticked at regular intervals"
        echo = random.choice(ECHOES)
        self.msg_contents(echo)
"""