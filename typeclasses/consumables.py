from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia import Command
from evennia import CmdSet
from evennia import create_object
from config.configlists import CONSUMABLE_MESSAGE_TYPES
from typeclasses.scripts import DrugUse


# == == == == == Here are the consumable object types == == == == == == #

class EatOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
        if not self.db.messages:
            self.db.messages = {message: "" for message in CONSUMABLE_MESSAGE_TYPES}

class DrinkOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
        if not self.db.messages:
            self.db.messages = {message: "" for message in CONSUMABLE_MESSAGE_TYPES}

class SmokeOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
           if not self.db.messages:
                self.db.messages = {message: "" for message in CONSUMABLE_MESSAGE_TYPES}
    
class DrugOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
           if not self.db.messages:
                self.db.messages = {message: "" for message in CONSUMABLE_MESSAGE_TYPES}


# == == == == == Here are the consumable object commands == == == == == == #

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


# == == == == == Here are the commands for actually CONSUMING == == == == == == #


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
        target = self.caller.search(toeat, candidates=self.caller.contents, typeclass=EatOb)
        

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
        target = self.caller.search(todrink, candidates=self.caller.contents, typeclass=DrinkOb)

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

class CmdDose(Command):
    """
    Usage: 
        dose <thing>
        allows you to take a consumable drug!
    """
    key = 'dose'
    aliases = ("pop")
    def func(self):
        if not self.args:
            self.msg("Usage: dose <drug>")
            return

        todose = self.args.strip()
        target = self.caller.search(todose, candidates=self.caller.contents, typeclass=DrugOb)

        if not target: 
            self.msg("You don't have anything dosable by that name.")
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

class CmdRail(Command):
    """
    Usage: 
        rail <thing>
        allows you knock back all of a drug at once.
    """
    key = 'rail'
    def func(self):
        if not self.args:
            self.msg("Usage: rail <drug>")
            return

        torail = self.args.strip()
        target = self.caller.search(torail, candidates=self.caller.contents, typeclass=DrugOb)

        if not target: 
            self.msg("You don't have anything to RAIL by that name.")
            return
        else:
            if target.location == self.caller:
                self.caller.msg(target.db.messages['chug_msg'])
                target.delete()
                self.caller.scripts.add(DrugUse)

# == == == == == Here is the object creation command == == == == == == #


class CmdCreateObj(Command):
    """
    Usage:
        @CreateObj <type> = name
    """
    key = "@createobj"
    locks = "cmd:perm(Builders)"
    help_category = "Builders"

    def func(self):
        caller = self.caller
        if not self.args:
            self.msg("Usage: @createobj <type> = name")
            return

        self.object_type, self.name = self.args.split('=')
        self.object_type = self.object_type.strip()
        self.name = self.name.strip()

        obj_name = self.name
        obj_type = self.object_type
        self.caller.msg("Creating object type %s" % obj_type)
        food = create_object(typeclass=obj_type,
                             key=obj_name,
                             location=self.caller.location)
        food.db.desc = "A generic %s object." % obj_type
        food.db.value = 1
        food.db.portions = 3



# == == == == == Here are the consumable object command sets == == == == == == #

class ConsumableCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdEat())
        self.add(CmdDrink())
        self.add(CmdDose())
        self.add(CmdRail())

class ConsumableBuildSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCreateObj())
        self.add(CmdSetConMsg())
        self.add(CmdSetOConMsg())
        self.add(CmdSetFinishMsg())
