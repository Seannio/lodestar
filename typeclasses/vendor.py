# mygame/typeclasses/vendor.py

from evennia import DefaultRoom, DefaultExit, DefaultObject

from evennia.utils.create import create_object
from evennia.utils import evmenu
from evennia import Command
from evennia import CmdSet

def menunode_shopfront(caller):
    "This is the top-menu screen."

    shopname = caller.location.key
    wares = caller.location.db.storeroom.contents

    # Wares includes all items inside the storeroom, including the
    # door! Let's remove that from our for sale list.
    wares = [ware for ware in wares if ware.key.lower()]

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

    wares = caller.location.contents
    # Don't forget, we will need to remove that pesky door again!
    wares = [ware for ware in wares if ware.key.lower()]
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
        if not self.args:
            self.msg("Usage: buy <shop name>")
            return

        "Starts the shop EvMenu instance"
        shopname = self.args.strip()
        locationkeys = self.caller.location.contents
        self.msg("shopname : %s" % shopname)
        self.msg("locationkeys : %s" % locationkeys)

        for ob in locationkeys:
            if shopname in ob:
                self.msg("Object: %s matches shopname" % ob)
            if shopname not in ob:
                self.msg("There's no shop by that name here.")
                return
            


        evmenu.EvMenu(self.caller, 
                      "typeclasses.vendor",
                      shopname,
                      startnode="menunode_shopfront")

class CmdBuildShop(Command):
    """
    Build a new shop

    Usage:
        @buildshop shopname

    This will create a new VENDING MACHINE object, where
    the items to be sold will be stored in the vending machine. 
    """
    key = "@buildshop"
    locks = "cmd:perm(Builders)"
    help_category = "Builders"

    def func(self):
        "Create the shop objects"
        if not self.args:
            self.msg("Usage: @buildshop <storename>")
            return
        # create the shop and storeroom
        shopname = self.args.strip()
        shop = create_object(VendingMachine,
                             key=shopname,
                             location=self.caller.location)
        shop.db.storeroom = shop

        # inform the builder about progress
        self.caller.msg("The shop %s was created!" % shop)
        self.caller.msg("The contents of the shop are %s" % shop.contents)


class ShopCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdBuy())

# bottom of mygame/typeclasses/npcshop.py

class VendingMachine(DefaultObject):
       "A basic vending machine object that can't be STOLEN."
       def at_object_creation(self):
           "Called whenever a new object is created"
           # lock the object down by default
           self.cmdset.add_default(ShopCmdSet)
           self.db.storeroom = None
           self.locks.add("get:false()")
           # the default "get" command looks for this Attribute in order
           # to return a customized error message (we just happen to know
           # this, you'd have to look at the code of the 'get' command to
           # find out).
           self.db.get_err_msg = "The vending machine is too heavy to pick up."

# class for our front shop room
class NPCShop(DefaultRoom):
    def at_object_creation(self):
        # we could also use add(ShopCmdSet, permanent=True)
        self.cmdset.add_default(ShopCmdSet)
        self.db.storeroom = None

class VendingMachine(DefaultObject):
       "A basic vending machine object that can't be STOLEN."
       def at_object_creation(self):
           "Called whenever a new object is created"
           # lock the object down by default
           self.cmdset.add_default(ShopCmdSet)
           self.db.storeroom = None
           self.locks.add("get:false()")
           # the default "get" command looks for this Attribute in order
           # to return a customized error message (we just happen to know
           # this, you'd have to look at the code of the 'get' command to
           # find out).
           self.db.get_err_msg = "The vending machine is too heavy to pick up."