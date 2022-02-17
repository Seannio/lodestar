"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    pass

class Character(DefaultCharacter):
    # [...]
    def at_object_creation(self):
        """
        Called only at initial creation. This is a rather silly
        example since ability scores should vary from Character to
        Character and is usually set during some character
        generation step instead.
            - For this purpose, we set every stat to 1 (base)
            # Synaptic_Tensility: Something about brain-wiggling, thought-bending 
            # Voltaic_Conception: Were you born technologically inclined, from a chrome-plated birthtube?
            # Superstitions: Don't you know it's bad luck to traverse space without carbon stiltbeads? 
            # Grey Augument: little by little, nanites form the tissue-base of your muscles. 
        """
        #set persistent attributes
        
        self.db.synaptic_tensility = 1
        self.db.voltaic_conception = 1
        self.db.superstitions = 1
        self.db.grey_augument = 1
        self.db.currency = 100


    def get_abilities(self):
        """
        Simple access method to return ability
        scores as a tuple (str,agi,mag)
        """
        return self.db.synaptic_tensility, self.db.voltaic_conception, self.db.superstitions,  self.db.grey_augument


    def get_currency(self):
        """
        Simple access method to return ability
        scores as a tuple (str,agi,mag)
        """
        return self.db.currency


    def at_pre_move(self, destination):
       """
       Called by self.move_to when trying to move somewhere. If this returns
       False, the move is immediately cancelled.
       """
       if self.db.is_resting:
           self.msg("You can't go anywhere while resting.")
           return False
       return True
