# mygame/typeclasses/vendor.py

from evennia import DefaultRoom, DefaultExit, DefaultObject

from evennia.utils.create import create_object
from evennia.utils import evmenu
from evennia import Command
from evennia import CmdSet

def menunode_shopfront(caller, raw_string):
    # First-screen for the Vending Machine
    # - Strips the shop-name from the args, populates the wares list with shop contents. 
    caller.ndb._menutree.shopname = raw_string.strip()
    
    vendobject = caller.search(caller.ndb._menutree.shopname, typeclass=VendingMachine)
    wares = vendobject.contents

    text = "*** Welcome to %s! ***\n" % caller.ndb._menutree.shopname
    if wares:
        text += "|wAn array of harshly-illuminated wares sit across the dipenser-display,\nsome out of stock\n|n (choose 1-%i to inspect,  quit to exit.)" \
             % len(wares)
    else:
        text += "The vending machine is empty."

    options = []
    for ware in wares:
        # add an option for every ware in store
        options.append({"desc": "%s (%s chits)" %
                             (ware.key, ware.db.gold_value or 1),
                        "goto": "menunode_inspect_and_buy"})
    return text, options

def menunode_inspect_and_buy(caller, raw_string):
    "Sets up the buy menu screen."

    vendobject = caller.search(caller.ndb._menutree.shopname, typeclass=VendingMachine)
    wares = vendobject.contents
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
        target = self.caller.search(shopname, typeclass=VendingMachine)
        if not target: 
            self.msg("There isn't a shop here by that name.")
            return
        evmenu.EvMenu(self.caller, 
                      "typeclasses.vendor",
                      startnode="menunode_shopfront",
                      cmd_on_exit="look",
                      startnode_input=shopname)
                      
        """
        locationkeys = self.caller.location.contents
        
        for key in locationkeys:
            if key.key == shopname:
                evmenu.EvMenu(self.caller, 
                      "typeclasses.vendor",
                      startnode="menunode_shopfront",
                      startnode_input=shopname)
            else:
                self.msg("There's no shop by that name here.")  
        """

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
