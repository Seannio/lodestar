"""
Room

Rooms are simple containers that has no location of their own.

"""
import random
from evennia import DefaultRoom
from random import choice
from evennia import TICKER_HANDLER
from collections import defaultdict
from typeclasses.characters import Character
from typeclasses.furniture import SittableOb



class Room(DefaultRoom):

    def return_appearance(self, looker, **kwargs):
        if not looker:
            return ""
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exits, players, seats, things = [], [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(key)
            elif con.is_typeclass(Character):
                if con.db.temp_idlepose:
                    players.append("|c%s|n %s" % (key, con.db.temp_idlepose))
                else:
                    players.append("|c%s|n %s" % (key, con.db.idlepose))
            elif con.is_typeclass(SittableOb):
                seats.append("|na %s" % key)
            else:
                things[key].append(con)

        string = "|c%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc

        if desc:
            string += "%s" % desc
        if players:
            string += "\n|n" + ' '.join(players) 

        string += "\n"

        if things:
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]
                thing_strings.append(key)
            string += "\n|wYou see:|n " + ', '.join(thing_strings)
        if seats:
            string += "\n|wSeats:|n " + ', '.join(seats)
        if exits:
            string += "\n|wExits:|n " + ', '.join(exits)
        return string

    def at_look(self, target, **kwargs):
        description = target.return_appearance(self, **kwargs)
        target.at_desc(looker=self, **kwargs)
        return description
    pass


class TickerRoom(Room):
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
                "|mGrenadine Spritz|n",
                "|xLey-Vodka Sour|n",
                "|gSpicy Cactus-Jack|n",
                "|xSmoke-Rakja Highball|n",
                "|rFlaming Bushwrangler|n" 
        ]

        randomcups = [ "crystalline martini glass",
                    "tall flute-glass",
                    "engraved, old-fashioned glass",
                    "simple crystal shot-glass",
                    "crystalline highball glass",
                    "curiously-shaped cocktail glass",
                    "shiny, thin-stemmed wineglass"

        ]

        ECHOES = ("A bespokely-dressed waiter delicately squeezes through the patrons, carefully carrying two glasses of " + random.choice(randomgoods) + " on a platter.",
                 "Over the quiet, ambient music, a touch of conversation picks up at a nearby table, followed by soft laughter.",
                 "From the depths of the cosmos beyond the window, hazy heatwaves distort the faraway colours in a momentary ripple.",
                 "Behind the bar, a busy clockwork creature whirrs to life, its spindly brass arms collecting the requisite bottles for a " + random.choice(randomgoods) + ".",
                 "Behind the bar, a creaky clockwork mixing-figure austerely shakes a drink with mechanical precision. It eventually pours a " + random.choice(randomgoods) + " into a " + random.choice(randomcups)+ ".",
                 "Behind the bar, a tired clockwork slicing-machine cuts up a variety of small fruit-pieces, depositing them into a bin for cocktailmaking.",
        )


        print("This is a regular ticker update, once for each room which calls it.")
        self.msg_contents("|n%s" % random.choice(ECHOES))


