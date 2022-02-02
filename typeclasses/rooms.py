"""
Room

Rooms are simple containers that has no location of their own.

"""
import random
from evennia import DefaultRoom
from random import choice
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

class TickerRoom(DefaultRoom):
    "This room is ticked at regular intervals"

    def at_object_creation(self):
        super().at_object_creation()
        "called only when the object is first created"
        TICKER_HANDLER.add(10, self.at_ticker_update)
        print("AAAAAAA. CREATED THING with TICKER!")

    def at_ticker_update(self, *args, **kwargs):

        randomgoods = ["reactor-plates.",
                "high-speed graphene batteries.",
                "dogs wearing hats.",
                "weapons-grade chili.",
                "illegally-sourced tubers." ]

        ECHOES = ["A forklift trundles by, carrying a huge pallet of  " + random.choice(randomgoods),
                 "A trickle of oil leaking from the ceiling-pipes splatters onto the ground nearby.",
                 "A deep, mechanical groan echoes down the length of the ship, sending shivers up the spine.",
                 "A mechanized loader rolls by on worn-down treads, hefting a pile of " + random.choice(randomgoods),
                 "Farther down the hangar, the sound of a dropped tool echoes dully against the high, metal walls." ]
       
        print(random.choice(ECHOES))

        "ticked at regular intervals"
        print("This is a regular ticker update.")
        self.msg_contents("|w%s|n" % random.choice(ECHOES))
