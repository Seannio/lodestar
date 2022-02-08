# mygame/typeclasses/vendor.py

from evennia.utils import evmenu
from evennia import Command
from evennia import CmdSet

def menunode_shopfront(caller):
    "This is the top-menu screen."

    shopname = caller.location.key
    wares = caller.location.db.storeroom.contents

    # Wares includes all items inside the storeroom, including the
    # door! Let's remove that from our for sale list.
    wares = [ware for ware in wares if ware.key.lower() != "door"]

    text = "*** Welcome to %s! ***\n" % shopname
    if wares:
        text += "   Things for sale (choose 1-%i to inspect);" \
                " quit to exit:" % len(wares)
    else:
        text += "   There is nothing for sale; quit to exit."

    options = []
    for ware in wares:
        # add an option for every ware in store
        options.append({"desc": "%s (%s chits)" %
                             (ware.key, ware.db.gold_value or 1),
                        "goto": "menunode_inspect_and_buy"})
    return text, options

def menunode_inspect_and_buy(caller, raw_string):
    "Sets up the buy menu screen."

    wares = caller.location.db.storeroom.contents
    # Don't forget, we will need to remove that pesky door again!
    wares = [ware for ware in wares if ware.key.lower() != "door"]
    iware = int(raw_string) - 1
    ware = wares[iware]
    value = ware.db.gold_value or 2
    wealth = caller.db.gold or 0
    text = "You inspect %s:\n\n%s" % (ware.key, ware.db.desc)

    def buy_ware_result(caller):
        "This will be executed first when choosing to buy."
        if wealth >= value:
            rtext = "You pay %i chits and purchase %s!" % \
                         (value, ware.key)
            caller.db.gold -= value
            ware.move_to(caller, quiet=True)
        else:
            rtext = "You cannot afford %i chits for %s!" % \
                          (value, ware.key)
        caller.msg(rtext)

    options = ({"desc": "Buy %s for %s gold" % \
                        (ware.key, ware.db.gold_value or 1),
                "goto": "menunode_shopfront",
                "exec": buy_ware_result},
               {"desc": "Look for something else",
                "goto": "menunode_shopfront"})

    return text, options
    # mygame/typeclasses/npcshop.py
class CmdBuy(Command):
    """
    Start to do some shopping

    Usage:
      buy
      shop
      browse

    This will allow you to browse the wares of the
    current shop and buy items you want.
    """
    key = "buy"
    aliases = ("shop", "browse")

    def func(self):
        "Starts the shop EvMenu instance"
        evmenu.EvMenu(self.caller,
                      "typeclasses.vendor",
                      startnode="menunode_shopfront")

class ShopCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdBuy())

# bottom of mygame/typeclasses/npcshop.py

from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia.utils.create import create_object



# class for our front shop room
class NPCShop(DefaultRoom):
    def at_object_creation(self):
        # we could also use add(ShopCmdSet, permanent=True)
        self.cmdset.add_default(ShopCmdSet)
        self.db.storeroom = None

