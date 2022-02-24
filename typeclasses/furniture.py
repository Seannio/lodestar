from evennia import InterruptCommand 
from evennia import DefaultObject
from evennia import Command, CmdSet
from config.configlists import FURNITURE_MESSAGE_TYPES

class SittableOb(DefaultObject):

    def at_object_creation(self):
        self.db.sitting = []
        self.db.space = 1
        self.locks.add("get:false()")
        self.db.get_err_msg = "The %s is too heavy to pick up." % self.db.name

        if not self.db.messages:
            self.db.messages = {message: " " for message in FURNITURE_MESSAGE_TYPES}

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this SittableOb object.

        Args:
            sitter (Object): The one trying to sit down.
        """
        sitter.db.seat = self.key
        current = self.db.sitting
        print("NOW.... LEN of the SITTING ARRAY: %i" % len(self.db.sitting))
        print(" VERSUS LEN of the sitting space: %i" % self.db.space)
        if sitter in current:
            sitter.msg("You are already sitting on %s." % self.key)
        elif len(self.db.sitting) >= self.db.space:
            sitter.msg( "There's no space left on %s" % self.key)
        else: 
            self.db.sitting.append(sitter)
            sitter.db.is_sitting= True
            print(self.db.sitting)
            sitter.msg(self.db.messages['sit_msg'])
            sitter.location.msg_contents(self.db.messages['osit_msg'], exclude=sitter)

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.
        """
        current = self.db.sitting
        try:
            if not stander in current:
                stander.msg("You are not sitting on %s." % self.key)
            else:
                self.db.sitting.remove(stander)
                stander.db.is_sitting = False
                stander.db.seat = None
                stander.msg(self.db.messages['stand_msg'])
                stander.location.msg_contents(self.db.messages['ostand_msg'], exclude=stander)
                #stander.msg(f"You stand up from {self.key}")
        except AttributeError:
            stander.msg("You're not sitting.")
            stander.db.is_sitting = False

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

    def parse(self):
        if self.caller.db.is_sitting is False:
            self.caller.msg("Try sitting on something before standing up. ")
            raise InterruptCommand

    def func(self):
        caller = self.caller
        sittable = self.caller.search(
                         self.caller.db.seat,
                         candidates=self.caller.location.contents,
                         typeclass="typeclasses.furniture.SittableOb")

        if not sittable:
            return

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



class CmdSetOSitMsg(Command):
    '''
    Set the room message when sitting on a furniture object
    Usage: @osit_msg furniture = <message>
    '''
    key = '@osit_msg'
    locks = "cmd:perm(Builders)"
    help_category = "furniture"

    def parse(self):
        if not self.args:
            self.msg("Usage: @osit_msg <item> = <message>")
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
                furniture.db.messages['osit_msg'] = self.msg.strip()
                caller.msg("osit_msg for %s set as: %s" % (furniture.name, self.msg.strip()))

class CmdSetOStandMsg(Command):
    '''
    Set the external message when standing from a furniture object
    Usage: @ostand_msg furniture = <message>
    '''
    key = '@ostand_msg'
    locks = "cmd:perm(Builders)"
    help_category = "furniture"

    def parse(self):
        if not self.args:
            self.msg("Usage: @ostand_msg <item> = <message>")
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
                furniture.db.messages['ostand_msg'] = self.msg.strip()
                caller.msg("ostand_msg for %s set as: %s" % (furniture.name, self.msg.strip()))


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

class CmdSetSpace(Command):
    '''
    Set the space on a seat
    Usage: @seat_space furniture = num
    '''
    key = '@seat_space'
    locks = "cmd:perm(Builders)"
    help_category = "furniture"

    def parse(self):
        if not self.args:
            self.msg("Usage: @ostand_msg <item> = <message>")
            return

    def func(self):
        caller = self.caller
        self.searchob, self.seats = self.args.split('=')
        self.searchob = self.searchob.strip()
        self.seats = self.seats.strip()

        if self.seats:
            seatobj = self.caller.search(self.searchob, candidates=self.caller.location.contents)
            if not seatobj:
                self.caller.msg("Thing to set seats for should be on the floor.")
                return
            if self.searchob:
                seatobj.db.space = int(self.seats)
                caller.msg("Seat-amount for %s set as: %s" % (seatobj.name, self.seats))


class SitCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSit)
        self.add(CmdStand)

class FurnitureBuildSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSetSitMsg())
        self.add(CmdSetStandMsg())
        self.add(CmdSetOSitMsg())
        self.add(CmdSetOStandMsg())
        self.add(CmdSetSpace())