from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia import Command
from evennia import CmdSet
from evennia import create_object

class ConsumableObject(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       def at_object_creation(self):
           consume_msg = "Wakakskaks"

           gold_value = 100

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
                self.caller.msg_contents(target.db.oconsume_msg)
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