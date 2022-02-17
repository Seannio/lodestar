"""
Room

Rooms are simple containers that has no location of their own.

"""
import random
from evennia import DefaultRoom
from random import choice
from evennia import TICKER_HANDLER
from collections import defaultdict
from commands.default_cmdsets import ChargenCmdset


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

class ChargenRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(ChargenCmdset, permanent=True)







class TickerRoom(DefaultRoom):
    "This room is ticked at regular intervals"

    def at_object_creation(self):
        super().at_object_creation()
        TICKER_HANDLER.add(300, self.at_ticker_update)
        print("Created ticker")

    def at_ticker_update(self, *args, **kwargs):
        randomgoods = [ "|ySandmelt Vibrofruit Martini|n",
                "|wWhite Ruskovian|n",
                "|YGolden Stopwatch cocktail|n",
                "|!RTwelve-Mango Special|n",
                "|CMageweaver's Menta|n",
                "|yBrewer's Pudding|n",
                "|gBackalley Bog Grog|n",
                "|mGrenadine and Spritz|n",
                "|xLey-Vodka Sour|n",
                "|gSpicy Cactus-Jack|n",
                "|xSmoke-Rakja Highball|n",
                "|rFlaming Bushwrangler|n" 
        ]

        ECHOES = ("A bespokely-dressed waiter delicately squeezes through the patrons, carefully carrying a platter of " + random.choice(randomgoods) + "s.",
                 "Over the quiet, ambient music, a touch of conversation picks up at a nearby table, followed by soft laughter.",
                 "From the depths of the cosmos beyond the window, hazy heatwaves distort the faraway colours in a momentary ripple.",
                 "Behind the bar, a busy clockwork creature whirrs to life, its spindly brass arms collecting the requisite bottles for a " + random.choice(randomgoods) + ".",
                 "Behind the bar, a creaky clockwork mixing-figure austerely shakes a drink with mechanical precision. It eventually pours a " + random.choice(randomgoods) + " into a fine glass.",
                 "Behind the bar, a tired clockwork slicing-machine cuts up a variety of small fruit-pieces, depositing them into a bin for cocktailmaking.",
        )


        print("This is a regular ticker update, once for each room which calls it.")
        self.msg_contents("|n%s" % random.choice(ECHOES))


