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
            self.db.messages = {message: " " for message in CONSUMABLE_MESSAGE_TYPES}
            self.db.value = 1
            self.db.portions = 1

class DrinkOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
        if not self.db.messages:
            self.db.messages = {message: " " for message in CONSUMABLE_MESSAGE_TYPES}
            self.db.value = 1
            self.db.portions = 1

class SmokeOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
           if not self.db.messages:
                self.db.messages = {message: " " for message in CONSUMABLE_MESSAGE_TYPES}
                self.db.value = 1
                self.db.portions = 1

class DrugOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
           if not self.db.messages:
                self.db.messages = {message: " " for message in CONSUMABLE_MESSAGE_TYPES}
                self.db.value = 1
                self.db.portions = 1

# == == == == == Here are the consumable object commands == == == == == == #

class CmdSetConMsg(Command):
    '''
    Sets the local (internal) message when consuming a consumable
    Usage: @con_msg <consumable item> = <message>
    '''

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
    '''
    Sets the room (external) message when consuming a consumable
    Usage: @oconn_msg <consumable item> = <message>
    '''

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
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                connsumableobj.db.messages['ocon_msg'] = self.msg
                caller.msg("ocon_msg for %s set as: %s" % (connsumableobj.name, self.msg))


class CmdSetFinishMsg(Command):
    '''
    Sets the local (internal) message when finishing a consumable
    Usage: @finish_msg <consumable item> = <message>
    '''

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
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                connsumableobj.db.messages['finish_msg'] = self.msg
                caller.msg("finish_msg for %s set as: %s" % (connsumableobj.name, self.msg))

class CmdSetOFinishMsg(Command):
    '''
    Sets the room (external) message when finishing a consumable
    Usage: @ofinish_msg <consumable item> = <message>
    '''

    key = '@ofinish_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @ofinish_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.msg = self.msg.strip()

        if self.msg:
            connsumableobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                connsumableobj.db.messages['ofinish_msg'] = self.msg
                caller.msg("ofinish_msg for %s set as: %s" % (connsumableobj.name, self.msg))

class CmdSetChugMsg(Command):
    '''
    Sets the local (internal) message when chugging/railing a consumable
    Usage: @chug_msg <consumable item> = <message>
    '''

    key = '@chug_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @chug_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.msg = self.msg.strip()

        if self.msg:
            connsumableobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                connsumableobj.db.messages['chug_msg'] = self.msg
                caller.msg("chug_msg for %s set as: %s" % (connsumableobj.name, self.msg))

class CmdSetOChugMsg(Command):
    '''
    Sets the room (external) message when chugging/railing a consumable
    Usage: @ochug_msg <consumable item> = <message>
    '''

    key = '@ochug_msg'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @ochug_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.msg = self.msg.strip()

        if self.msg:
            connsumableobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not connsumableobj:
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                connsumableobj.db.messages['ochug_msg'] = self.msg
                caller.msg("ochug_msg for %s set as: %s" % (connsumableobj.name, self.msg))

class CmdSetValue(Command):
    '''
    Sets the value for a consumable
    Usage: @setvalue <consumable item> = <value>
    '''
    key = '@setvalue'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @setvalue <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.val = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.val = self.val.strip()

        if self.val:
            valueobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not valueobj:
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                valueobj.db.value = int(self.val)
                caller.msg("value for %s set as: %s" % (valueobj.name, self.val))

class CmdSetPortions(Command):
    '''
    Sets the value for a consumable
    Usage: @setpor <consumable item> = <value>
    '''
    key = '@setpor'
    locks = "cmd:perm(Builders)"
    help_category = "consumables"

    def parse(self):
        if not self.args:
            self.msg("Usage: @setpor <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.val = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.val = self.val.strip()

        if self.val:
            valueobj = self.caller.search(self.searchob, candidates=self.caller.contents)
            if not valueobj:
                self.caller.msg("Thing to set message for must be in inv.")
                return
            if self.searchob:
                valueobj.db.portions = int(self.val)
                caller.msg("value for %s set as: %s" % (valueobj.name, self.val))


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
                    self.caller.location.msg_contents(target.db.messages['ocon_msg'], exclude=self.caller)
                    target.db.portions -= 1
                elif target.db.portions == 1:
                    self.caller.msg(target.db.messages['finish_msg'])
                    self.caller.location.msg_contents(target.db.messages['ofinish_msg'], exclude=self.caller)
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
                    self.caller.location.msg_contents(target.db.messages['ocon_msg'], exclude=self.caller)
                    target.db.portions -= 1
                elif target.db.portions == 1:
                    self.caller.msg(target.db.messages['finish_msg'])
                    self.caller.location.msg_contents(target.db.messages['ofinish_msg'], exclude=self.caller)
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
                    self.caller.location.msg_contents(target.db.messages['ocon_msg'], from_obj=self.caller, exclude=self.caller)
                    target.db.portions -= 1
                elif target.db.portions == 1:
                    self.caller.msg(target.db.messages['finish_msg'])
                    self.caller.location.msg_contents(target.db.messages['ofinish_msg'], from_obj=self.caller, exclude=self.caller)
                    target.delete()

class CmdSmoke(Command):
    """
    Usage: 
        smoke <thing>
        allows you to smoke something!
    """
    key = 'smoke'
    aliases = ("toke")
    def func(self):
        if not self.args:
            self.msg("Usage: smoke <thing>")
            return

        tosmoke = self.args.strip()
        target = self.caller.search(tosmoke, candidates=self.caller.contents, typeclass=SmokeOb)

        if not target: 
            self.msg("You don't have anything dosable by that name.")
            return
        else:
            if target.location == self.caller:
                if target.db.portions != 1:
                    self.caller.msg(target.db.messages['con_msg'])
                    self.caller.location.msg_contents(target.db.messages['ocon_msg'], exclude=self.caller)
                    target.db.portions -= 1
                elif target.db.portions == 1:
                    self.caller.msg(target.db.messages['finish_msg'])
                    self.caller.location.msg_contents(target.db.messages['ofinish_msg'], exclude=self.caller)
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
                self.caller.location.msg_contents(target.db.messages['ochug_msg'], exclude=self.caller)
                target.delete()
                self.caller.scripts.add(DrugUse)


class CmdChug(Command):
    """
    Usage: 
        chug <thing>
        allows you knock back all of a drink at once.
    """
    key = 'chug'
    def func(self):
        if not self.args:
            self.msg("Usage: chug <drink>")
            return

        tochug= self.args.strip()
        target = self.caller.search(tochug, candidates=self.caller.contents, typeclass=DrinkOb)

        if not target: 
            self.msg("You don't have anything to CHUG by that name.")
            return
        else:
            if target.location == self.caller:
                self.caller.msg(target.db.messages['chug_msg'])
                self.caller.location.msg_contents(target.db.messages['ochug_msg'], exclude=self.caller)
                target.delete()

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
        elif '=' not in self.args:
            self.msg("Usage: @createobj <type> = name")
            return

        self.object_type, self.name = self.args.split('=')
        self.object_type = self.object_type.strip()
        self.name = self.name.strip()

        obj_name = self.name
        obj_type = self.object_type
        self.caller.msg("Creating object type %s" % obj_type)
        obj = create_object(typeclass=obj_type,
                             key=obj_name,
                             location=self.caller.location)
        obj.db.desc = "A generic %s object." % obj_type
        obj.db.value = 1
        obj.db.portions = 3



# == == == == == Here are the consumable object command sets == == == == == == #

class ConsumableCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdEat())
        self.add(CmdDrink())
        self.add(CmdSmoke())
        self.add(CmdDose())
        self.add(CmdChug())
        self.add(CmdRail())

class ConsumableBuildSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCreateObj())
        self.add(CmdSetConMsg())
        self.add(CmdSetOConMsg())
        self.add(CmdSetFinishMsg())
        self.add(CmdSetOFinishMsg())
        self.add(CmdSetChugMsg())
        self.add(CmdSetOChugMsg())
        self.add(CmdSetValue())
        self.add(CmdSetPortions())
