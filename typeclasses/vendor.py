# mygame/typeclasses/vendor.py

from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia.utils.create import create_object
from evennia.utils import evmenu
from evennia import Command
from evennia import CmdSet



def menunode_shopfront(caller, raw_string, **kwargs):

    # menu_dic is passed from kwargs, but is stored innately in
    # ndb._menutree. It's deleted on menu-exit. 
    menu_dic = caller.ndb._menutree.menu_dic
    cmdarg = menu_dic['shopname']

    # try-catch, forcing an error if multiple identical vending machines exist
    try:
        vendobject = caller.search(cmdarg, typeclass=VendingMachine)
        caller.ndb._menutree.shoptitle = vendobject
        wares = vendobject.contents
    except:
        caller.msg("Multiple identical machines! Please specify.")
        return

    # generate the MACHINE MENU! Maybe randomize things here, later.
    text = "*** Welcome to the %s service! ***\n" % caller.ndb._menutree.shoptitle
    if wares:
        text += "|wAn array of harshly-illuminated wares sit across the dipenser-display,\nsome out of stock\n|n (choose 1-%i to inspect,  quit to exit.)" \
             % len(wares)
    else:
        text += "The vending machine is empty."
    options = []
    for ware in wares:
        # list every ware in the store
        options.append({"desc": "%s (%s chits)" %
                             (ware.key, ware.db.value or 1),
                        "goto": "menunode_inspect_and_buy"})
    return text, options

def menunode_inspect_and_buy(caller, raw_string):
    # called by "goto" in the previous function
    #vendobject = caller.search(caller.ndb._menutree.shoptitle, typeclass=VendingMachine)
    wares = caller.ndb._menutree.shoptitle.contents

    iware = int(raw_string) - 1
    ware = wares[iware]
    value = ware.db.value or 1
    wealth = caller.db.currency or 0
    text = "You inspect %s:\n\n%s" % (ware.key, ware.db.desc)

    def buy_ware_result(caller):
        "This will be executed first when choosing to buy."
        if wealth >= value:
            rtext = "\n|wYou feed %i pieces of currency into the %s. After a second, it beeps and dispenses your %s!" % \
                         (value, caller.ndb._menutree.shoptitle, ware.key)
            caller.db.currency -= value
            ware.move_to(caller, quiet=True)
            caller.location.msg_contents("%s feeds some currency into the %s's payment-slot and withdraws an item." % (caller.key, caller.ndb._menutree.shoptitle), exclude=caller)
        else:
            rtext = "\n|wThe %s makes a loud, offensive buzz as you attempt to pay for your stuff. You cannot afford %i chits for %s!" % \
                          (caller.ndb._menutree.shoptitle, value, ware.key)
            caller.location.msg_contents("%s presses a few buttons on the %s, eliciting a loud |rBEEEP." % (caller.key, caller.ndb._menutree.shoptitle), exclude=caller)
        caller.msg(rtext)
        

    options = ({"desc": "Buy %s for %s gold" % \
                        (ware.key, ware.db.value or 1),
                "goto": ('menunode_shopfront'),
                "exec": buy_ware_result},
               {"desc": "Look for something else",
                "goto": ('menunode_shopfront')}
               )

    return text, options

# ------- Vendor Commands  --------

class CmdCreateVend(Command):
    """
    Build a new shop

    Usage:
        @createvend <vending machine name>

    This will create a new, empty VENDING MACHINE object. 
    They can be loaded with stuff via the <stock> command.
    """
    key = "@createvend"
    locks = "cmd:perm(Builders)"
    help_category = "Builders"

    def func(self):
        "Create the shop objects"
        if not self.args:
            self.msg("Usage: @createvend <vending machine name>")
            return

        # create the shop 
        shopname = self.args.strip()
        shop = create_object(VendingMachine,
                             key=shopname,
                             location=self.caller.location)
        shop.db.desc = "A strange-looking vending machine."
        shop.db.storeroom = shop

        # inform the builder about progress
        self.caller.msg("The shop %s was created!" % shop)
        self.caller.msg("The contents of the shop are %s" % shop.contents)

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

        menu_dic = {'shopname':shopname, 'char_class': None}

        evmenu.EvMenu(self.caller, 
                      "typeclasses.vendor",
                      startnode="menunode_shopfront",
                      cmd_on_exit="look",
                      startnode_input=shopname,
                      menu_dic=menu_dic)

class CmdStock(Command):
    """
    Usage: 
        stock <vending machine> with <goods>
        Loads a vending machine with OBJECTS.  
    """
    key = 'stock'
    aliases = ("load")

    #TODO: Make refactor the Stock item to deposit multiples of something!

    def parse(self):
        if not self.args:
            self.msg("Usage: stock <machine> with <goods>")
            return
        self.machine_arg, self.goods_arg = self.args.split('with')
        self.goods_arg = self.goods_arg.strip()
        self.machine_arg = self.machine_arg.strip()

    def func(self):
        caller = self.caller
        goods_arg = self.goods_arg
        machine_arg = self.machine_arg

        # Find the item.
        # Location unset, search conducted within the character and its location.

        item = caller.search(goods_arg, quiet=True)
        if item:
            if len(item):
                item = item[0]
            container = caller.search(machine_arg, quiet=True)
            if container:
                if len(container):
                    container = container[0]
                if item.location == caller:
                    caller.msg(f"You place {item.name} in {container.name}.")
                    caller.msg_contents(f"{caller.name} places {item.name} in {container.name}.", exclude=caller)
                elif item.location == caller.location:
                    caller.msg(f"You pick up {item.name} and place it in {container.name}.")
                    caller.msg_contents(f"{caller.name} picks up {item.name} and places it in {container.name}.", exclude=caller)
                item.move_to(container, quiet=True)
            else:
                caller.msg(f"Could not find {machine_arg}!")
        else:
            caller.msg(f"Could not find {goods_arg}!")


# ------- Vendor Objects  --------

class VendingMachine(DefaultObject):
       # a basic vending machine object with a get/move lock.
       def at_object_creation(self):
           # lock the object down by default
           self.locks.add("get:false()")
           self.db.get_err_msg = "The vending machine is too heavy to pick up."

class VendingStock(DefaultObject):
       # A basic vending machine object that can be stocked in a vending machine.
       # Ideally, when stocked, it should create several other objects. 
       # ex:  'crate of bottles' -> 5 bottles when placed

       # TODO: Make this an actual funcntioning thing.

       def at_object_creation(self):
           print("wow")

class ShopCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdBuy())
        self.add(CmdStock())