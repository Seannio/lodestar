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
               ["\nOn the tiny holopanel: An ad for Astro Lite, the universe's favorite lager brewed in space!",
                "\nOn the tiny holopanel: A technicolor ad for the wonders of flesh-eating nanites. ",
                "\nOn the tiny holopanel: A dead rat spinning perpetually.",
                "\nOn the tiny holopanel: A hat with fuzzy legs dancing to some out-of-date polka.",
                "\nOn the tiny holopanel: A static picture of a frog with six eyes, imploring you to invest in a company named TOADLICK." ]

    def return_appearance(self, looker):
        """
        Called by the look command. We want to return the tv screen:
        """
        # first get the base string from the
        # parent's return_appearance.
        string = super().return_appearance(looker)
        wisewords = choice(self.db.tv_texts)
        return string + wisewords

        