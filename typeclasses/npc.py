from characters import Character

class Npc(Character):
    """
    A NPC typeclass which extends the character class.
    """
    def at_heard_say(self, message, from_obj):
        """
        A simple listener and response. This makes it easy to change for
        subclasses of NPCs reacting differently to says.

        """
        # message will be on the form `<Person> says, "say_text"`
        # we want to get only say_text without the quotes and any spaces
        message = message.split('says, ')[1].strip(' "')

        # we'll make use of this in .msg() below
        return "%s said: '%s'" % (from_obj, message)