from random import choice
from typeclasses.objects import Object

class ScreenObject(Object):
    """
    An object that returns randomized text when someone looks at it, for the purpose of
    adds or etc. 
    """
    def at_object_creation(self):
        """Called when object is first created"""
        self.db.tv_texts = \
               ["On the tiny holopanel: An ad for Astro Lite, the universe's favorite lager brewed in space!",
                "On the tiny holopanel: A technicolor ad for the wonders of flesh-eating nanites. ",
                "On the tiny holopanel: a dead rat spinning perpetually." ]

    def return_appearance(self, looker):
        """
        Called by the look command. We want to return the tv screen:
        """
        # first get the base string from the
        # parent's return_appearance.
        string = super().return_appearance(looker)
        wisewords = choice(self.db.tv_texts)
        return string + wisewords

        