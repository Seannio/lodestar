from random import choice
from typeclasses.objects import Object
from config.configlists import SCREENOBJECT_STRINGS

class ScreenObject(Object):
    """
    An object that returns randomized text when someone looks at it, for the purpose of
    adds or etc. 
    """
    def at_object_creation(self):
        """Called when object is first created"""
        self.db.tv_texts = SCREENOBJECT_STRINGS


    def return_appearance(self, looker):
        """
        Called by the look command. We want to return the tv screen:
        """
        # first get the base string from the
        # parent's return_appearance.
        string = super().return_appearance(looker)
        randomad = choice(self.db.tv_texts)
        return string + randomad

        