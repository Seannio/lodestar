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

class CmdSetConMsg(Command):
    """
    Set the con_msg for a consumable 
    Usage:
        @con_msg <consumable item> = <message>
    """

    key = '@con_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Need to provide fooditem and message.")
            return

        if self.lhs:
            connsumableobj = self.caller.search(self.lhs, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be held.")
                return
            if self.rhs:
                connsumableobj.db.messages['con_msg'] = self.rhs
                caller.msg("Worn message for %s set as: %s" % (connsumableobj.name, self.rhs))


class CmdSetOConMsg(Command):
    """
    Set the ocon_msg for a consumable 
    Usage:
        @ocon_msg <consumable item> = <message>
    """

    key = '@ocon_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("Need to provide fooditem and message.")
            return

        if self.lhs:
            connsumableobj = self.caller.search(self.lhs, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be held.")
                return
            if self.rhs:
                connsumableobj.db.messages['ocon_msg'] = self.rhs
                caller.msg("Worn message for %s set as: %s" % (connsumableobj.name, self.rhs))



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
                self.caller.msg(target.db.consume_msg)
                self.caller.msg_contents(f"{self.caller.name} eats {target.name}.", exclude=self.caller)
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
        food.db.consume_msg = "You chow down on the %s" % food.key
        food.db.oconsume_msg = "%s chows down on their %s" % self.caller.name, food.key
        food.db.value = 50

# commandset for CONSUMING
class ConsumableCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdEat())

class ConsumableBuildSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCreateFood())
        self.add(CmdSetConMsg())
        self.add(CmdSetOConMsg())
