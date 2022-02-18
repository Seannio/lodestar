from evennia import DefaultRoom, DefaultExit, DefaultObject
from evennia import Command
from evennia import CmdSet
from evennia import create_object

class CurrencyOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
        self.db.value = 0

class CmdCurrency(Command):
        """
        Display your CASH.

        Usage:
          currency
        """
        key = "currency"
        aliases = ["cur", "count", "money"]
        lock = "cmd:all()"
        help_category = "Currency"

        def func(self):
            # pulls currency using get_currency in characters.py
            currency = self.caller.get_currency()
            string = "You do a brief count of the various currencies in your possession, eventually totalling: %sc.\n" % (currency)
            self.caller.msg(string)
            self.caller.msg_contents(f"{self.caller.name} searches through their belongings, taking a quick account of their cash.", exclude=self.caller)

class CmdPocket(Command):
    """
    Pocket a money-object into your character-stored money!  

    Usage:
          pocket (money object)
    """
    key = 'pocket'
    help_category = "Currency"
        
    def func(self):
        if not self.args:
            self.msg("Usage: pocket <money>")
            return

        topocket = self.args.strip()
        target = self.caller.search(topocket, candidates=self.caller.contents, typeclass=CurrencyOb)
        

        if not target: 
            self.msg("You've got no MONEY by that name!")
            return
        else:
            if target.location == self.caller:
                self.caller.db.currency += target.db.value
                self.msg("You pocket currency worth %s." % target.db.value )
                target.delete()

class CmdCashout(Command):
    """
    Turn your pocketed money into a currency object.
    Trying to cashout more than you have will result in you being scolded. 
    Usage:
          cashout (money object)
    """
    key = 'cashout'
    help_category = "Currency"
    def func(self):
        if not self.args:
            self.msg("Usage: cashout <amount>")
            return

        to_cashout = int(self.args.strip())

        if to_cashout > self.db.value:
            self.caller.msg("You don't have that much money, dumbass.")
        else:
            if to_cashout < 10:
                self.caller.msg("You count out a meagre amount of money into your palm.")
                obj = create_object(typeclass=CurrencyOb,
                             key="A small wad of cash.",
                             location=self.caller)
                obj.db.desc = "A small collection of coins, chits, stones, and bones worth roughly %s" % str(to_cashout)
                obj.db.value = to_cashout
                self.caller.db.currency -= to_cashout
            elif to_cashout > 10:
                self.caller.msg("You count out a big amount of money into your palm.")
                obj = create_object(typeclass=CurrencyOb,
                             key="A big wad of cash.",
                             location=self.caller)
                obj.db.desc = "A big collection of coins, chits, stones, and bones worth roughly %s" % str(to_cashout)
                obj.db.value = to_cashout
                self.caller.db.currency -= to_cashout


        

class CurrencyCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCurrency())
        self.add(CmdPocket())
        self.add(CmdCashout())