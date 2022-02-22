from evennia import InterruptCommand 
from evennia import DefaultObject
from evennia import Command, CmdSet
from config.configlists import FURNITURE_MESSAGE_TYPES

class SittableOb(DefaultObject):

    def at_object_creation(self):
        self.db.sitting = None
        if not self.db.messages:
            self.db.messages = {message: " " for message in FURNITURE_MESSAGE_TYPES}

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.

        Args:
            sitter (Object): The one trying to sit down.
        """

        current = self.db.sitting
        if current:
            if current == sitter:
                sitter.msg("You are already sitting on %s." % self.key)
            else:
                sitter.msg( "You can't sit on %s" % self.key)
            return

        self.db.sitting = sitter
        sitter.db.is_sitting= True
        sitter.msg(self.db.messages['sit_msg'])

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.
        """
        current = self.db.sitting
   
        if not stander == current:
            stander.msg("You are not sitting on %s." % self.key)
        else:
            self.db.sitting = None
            stander.db.is_sitting = False
            stander.msg(self.db.messages['stand_msg'])
            #stander.msg(f"You stand up from {self.key}")


class CmdSit(Command):
    """
    Sit down.

    Usage:
        sit <sittable>
    """
    key = "sit"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Sit on what?")
            raise InterruptCommand

    def func(self):
        sittable = self.caller.search(self.args)
        
        if not sittable:
            return
        elif self.caller.db.is_sitting == True:
            self.msg( "You are already sitting on something. Stand up first!")
            return
        try:
            sittable.do_sit(self.caller)
        except AttributeError:
            self.caller.msg("You can't sit on that!")

class CmdStand(Command):
    """
    Stand up.

    Usage:
        stand

    """
    key = "stand"

    def func(self):

        caller = self.caller
        # find the thing we are sitting on/in, by finding the object
        # in the current location that as an Attribute "sitter" set
        # to the caller
        if self.caller.db.is_sitting == False:
            self.caller.msg("You aren't sitting...")
            return

        try:
            sittable = self.caller.search(
                         self.caller,
                         candidates=self.caller.location.contents,
                         attribute_name="sitting",
                         typeclass="typeclasses.furniture.SittableOb")
        except AttributeError:
            self.caller.msg("You aren't sitting..")
            self.caller.db.is_sitting = False
    
        sittable.do_stand(caller)



# Set the messages for standing/sitting! 

class CmdSetSitMsg(Command):
    '''
    Set the internal message when sitting on a furniture object
    Usage: @sit_msg furniture = <message>
    '''
    key = '@sit_msg'
    locks = "cmd:perm(Builders)"
    help_category = "furniture"

    def parse(self):
        if not self.args:
            self.msg("Usage: @sit_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        if self.msg:
            furniture = self.caller.search(self.searchob.strip(), candidates=self.caller.location.contents, typeclass="typeclasses.furniture.SittableOb")
            if not furniture:
                self.caller.msg("This isn't a furniture object.")
                return
            if self.searchob:
                furniture.db.messages['sit_msg'] = self.msg.strip()
                caller.msg("sit_msg for %s set as: %s" % (furniture.name, self.msg.strip()))

class CmdSetStandMsg(Command):
    '''
    Set the internal message when standing from a furniture object
    Usage: @stand_msg furniture = <message>
    '''
    key = '@stand_msg'
    locks = "cmd:perm(Builders)"
    help_category = "furniture"

    def parse(self):
        if not self.args:
            self.msg("Usage: @stand_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.msg = self.args.split('=')
        if self.msg:
            furniture = self.caller.search(self.searchob.strip(), candidates=self.caller.location.contents, typeclass="typeclasses.furniture.SittableOb")
            if not furniture:
                self.caller.msg("This isn't a furniture object.")
                return
            if self.searchob:
                furniture.db.messages['stand_msg'] = self.msg.strip()
                caller.msg("stand_msg for %s set as: %s" % (furniture.name, self.msg.strip()))

class SitCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSit)
        self.add(CmdStand)

class FurnitureBuildSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSetSitMsg())
        self.add(CmdSetStandMsg())