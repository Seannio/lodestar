from evennia import DefaultCharacter
import re
from evennia.utils import logger
from evennia import DefaultCharacter

_GENDER_PRONOUN_MAP = {
    "male": {"s": "he", "o": "him", "p": "his", "a": "his"},
    "female": {"s": "she", "o": "her", "p": "her", "a": "hers"},
    "neutral": {"s": "it", "o": "it", "p": "its", "a": "its"},
    "ambiguous": {"s": "they", "o": "them", "p": "their", "a": "theirs"},
}
_RE_GENDER_PRONOUN = re.compile(r"(?<!\|)\|(?!\|)[sSoOpPaA]")

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
        super().at_object_creation()
        self.db.gender = "ambiguous"
        
        self.db.synaptic_tensility = 1
        self.db.voltaic_conception = 1
        self.db.superstitions = 1
        self.db.grey_augument = 1


        self.db.currency = 100


        self.db.is_sitting = False
        self.db.seat = None

    def _get_pronoun(self, regex_match):
        """
        Get pronoun from the pronoun marker in the text. This is used as
        the callable for the re.sub function.
        Args:
            regex_match (MatchObject): the regular expression match.
        Notes:
            - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
            - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
            - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
            - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs
        """
        typ = regex_match.group()[1]  # "s", "O" etc
        gender = self.attributes.get("gender", default="ambiguous")
        gender = gender if gender in ("male", "female", "neutral") else "ambiguous"
        pronoun = _GENDER_PRONOUN_MAP[gender][typ.lower()]
        return pronoun.capitalize() if typ.isupper() else pronoun

    def msg(self, text=None, from_obj=None, session=None, **kwargs):
        """
        Emits something to a session attached to the object.
        Overloads the default msg() implementation to include
        gender-aware markers in output.
        Args:
            text (str or tuple, optional): The message to send. This
                is treated internally like any send-command, so its
                value can be a tuple if sending multiple arguments to
                the `text` oob command.
            from_obj (obj, optional): object that is sending. If
                given, at_msg_send will be called
            session (Session or list, optional): session or list of
                sessions to relay to, if any. If set, will
                force send regardless of MULTISESSION_MODE.
        Notes:
            `at_msg_receive` will be called on this Object.
            All extra kwargs will be passed on to the protocol.
        """
        if text is None:
            super().msg(from_obj=from_obj, session=session, **kwargs)
            return

        try:
            if text and isinstance(text, tuple):
                text = (_RE_GENDER_PRONOUN.sub(self._get_pronoun, text[0]), *text[1:])
            else:
                text = _RE_GENDER_PRONOUN.sub(self._get_pronoun, text)
        except TypeError:
            pass
        except Exception as e:
            logger.log_trace(e)
        super().msg(text, from_obj=from_obj, session=session, **kwargs)

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


    def at_before_move(self, destination):
       """
       Called by self.move_to when trying to move somewhere. If this returns
       False, the move is immediately cancelled.
       """
       if self.db.is_sitting == True:
           self.db.is_sitting = True
           self.msg("Try standing up before moving!")
           return False

       return True




