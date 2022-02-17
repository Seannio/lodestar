from evennia import InterruptCommand 
from evennia import DefaultObject
from evennia import Command, CmdSet

class Sittable(DefaultObject):

    def at_object_creation(self):
        self.db.sitter = None

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.

        Args:
            sitter (Object): The one trying to sit down.
        """

        current = self.db.sitter
        if current:
            if current == sitter:
                sitter.msg(f"You are already sitting on {self.key}.")
            else:
                sitter.msg(
                    f"You can't sit on {self.key} "
                    f"- {current.key} is already sitting there!")
            return
        self.db.sitting = sitter
        sitter.db.is_resting = True
        sitter.msg(f"You sit on {self.key}")

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.

        """
        current = self.db.sitter
        if not stander == current:
            stander.msg(f"You are not sitting on {self.key}.")
        else:
            self.db.sitting = None
            stander.db.is_resting = False
            stander.msg(f"You stand up from {self.key}")


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
        seat = self.caller.search(self.args, typeclass=Sittable)
        if not seat:
            return
        try:
            seat.do_sit(self.caller)
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
        sittable = caller.search(
                         self.caller,
                         candidates=caller.location.contents,
                         attribute_name="sitter",
                         typeclass="typeclasses.furniture.Sittable")
        # if this is None, the error was already reported to user
        if not sittable:
            return

        sittable.do_stand(caller)


class SitCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdSit)
        self.add(CmdStand)