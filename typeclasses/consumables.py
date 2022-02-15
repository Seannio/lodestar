from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia import Command
from evennia import CmdSet
from evennia import create_object
from config.configlists import CONSUMABLE_MESSAGE_TYPES

class ConsumableObject(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'

       def at_object_creation(self):
           if not self.db.messages:
                self.db.messages = {message: "" for message in CONSUMABLE_MESSAGE_TYPES}

class DrinkableObject(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'

       def at_object_creation(self):
           if not self.db.messages:
                self.db.messages = {message: "" for message in CONSUMABLE_MESSAGE_TYPES}

class CmdSetConMsg(Command):
    """
    Set the con_msg for a consumable 
    Usage:
        @con_msg <consumable item> = <message>
    """

    key = '@con_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @con_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.msg = self.msg.strip()

        if self.msg:
            connsumableobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("This isn't a consumable object.")
                return
            if self.searchob:
                connsumableobj.db.messages['con_msg'] = self.msg
                caller.msg("con_msg for %s set as: %s" % (connsumableobj.name, self.msg))

class CmdSetOConMsg(Command):
    """
    Set the ocon_msg for a consumable 
    Usage:
        @ocon_msg <consumable item> = <message>
    """

    key = '@ocon_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @ocon_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.msg = self.msg.strip()

        if self.msg:
            connsumableobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be held.")
                return
            if self.searchob:
                connsumableobj.db.messages['ocon_msg'] = self.msg
                caller.msg("ocon_msg for %s set as: %s" % (connsumableobj.name, self.msg))


class CmdSetFinishMsg(Command):
    """
    Set the ocon_msg for a consumable 
    Usage:
        @finish_msg <consumable item> = <message>
    """

    key = '@finish_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @finish_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.msg = self.msg.strip()

        if self.msg:
            connsumableobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be held.")
                return
            if self.searchob:
                connsumableobj.db.messages['finish_msg'] = self.msg
                caller.msg("finish_msg for %s set as: %s" % (connsumableobj.name, self.msg))

class CmdEat(Command):
    """
    Usage: 
        eat <thing>
        allows you to eat a consumable object! 
    """
    key = 'eat'
    def func(self):
        if not self.args:
            self.msg("Usage: eat <edible thing>")
            return

        toeat = self.args.strip()
        target = self.caller.search(toeat, candidates=self.caller.contents, typeclass=ConsumableObject)
        

        if not target: 
            self.msg("You don't have anything edible by that name.")
            return
        else:
            if target.location == self.caller:
                if target.db.portions != 1:
                    self.caller.msg(target.db.messages['con_msg'])
                    self.caller.msg_contents(target.db.messages['ocon_msg'])
                    target.db.portions -= 1
                elif target.db.portions == 1:
                    self.caller.msg(target.db.messages['finish_msg'])
                    #TODO implement a ofinish message???
                    target.delete()


class CmdDrink(Command):
    """
    Usage: 
        drink <thing>
        allows you to eat a consumable object! 
    """
    key = 'drink'
    aliases = ("sip")
    def func(self):
        if not self.args:
            self.msg("Usage: drink <drinkable thing>")
            return

        todrink = self.args.strip()
        target = self.caller.search(todrink, candidates=self.caller.contents, typeclass=DrinkableObject)

        if not target: 
            self.msg("You don't have anything drinkable by that name.")
            return
        else:
            if target.location == self.caller:
                if target.db.portions != 1:
                    self.caller.msg(target.db.messages['con_msg'])
                    self.caller.msg_contents(target.db.messages['ocon_msg'])
                    target.db.portions -= 1
                elif target.db.portions == 1:
                    self.caller.msg(target.db.messages['finish_msg'])
                    #TODO implement a ofinish message???
                    target.delete()

class CmdCreateFood(Command):
    """
    Usage:
        @CreateFood food 
    """
    key = "@createfood"
    locks = "cmd:perm(Builders)"
    help_category = "Builders"

    def func(self):
        if not self.args:
            self.msg("Usage: @createfood food")
            return

        # create the shop 
        foodname = self.args.strip()
        self.caller.msg("Creating: %s" % foodname)
        food = create_object(ConsumableObject,
                             key=foodname,
                             location=self.caller.location)
        food.db.desc = "A generic food object."
        food.db.value = 2
        food.db.portions = 3

class CmdCreateDrink(Command):
    """
    Usage:
        @CreateDrink drink 
    """
    key = "@createdrink"
    locks = "cmd:perm(Builders)"
    help_category = "Builders"

    def func(self):
        if not self.args:
            self.msg("Usage: @createfood food")
            return

        # create the shop 
        foodname = self.args.strip()
        self.caller.msg("Creating: %s" % foodname)
        food = create_object(DrinkableObject,
                             key=foodname,
                             location=self.caller.location)
        food.db.desc = "A generic food object."
        food.db.value = 50
        food.db.portions = 3

# commandset for CONSUMING
class ConsumableCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdEat())
        self.add(CmdDrink())

class ConsumableBuildSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCreateFood())
        self.add(CmdSetConMsg())
        self.add(CmdSetOConMsg())
        self.add(CmdSetFinishMsg())
