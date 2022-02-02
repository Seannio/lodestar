"""
Room

Rooms are simple containers that has no location of their own.

"""
import random
from evennia import DefaultRoom, TICKER_HANDLER
from random import choice

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
        TICKER_HANDLER.add(10, self.at_weather_update)

    def at_weather_update(self, *args, **kwargs):
        "ticked at regular intervals"
        echo = random.choice(ECHOES)
        self.msg_contents(echo)
