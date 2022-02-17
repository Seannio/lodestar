
class CurrencyOb(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 
       # messages = 'con_msg', 'ocon_msg', 'value'
    def at_object_creation(self):
        self.db.value = 0

class CmdCurrency(BaseCommand):
        """
        Display your CASH.

        Usage:
          currency
        """
        key = "currency"
        aliases = ["cur", "count", "money"]
        lock = "cmd:all()"
        help_category = "General"

        def func(self):
            # pulls currency using get_currency in characters.py
            currency = self.caller.get_currency()
            string = "You do a brief count of the various currencies in your posession, eventually totalling: %sc.\n" % (currency)
            self.caller.msg(string)
            self.caller.msg_contents(f"{self.caller.name} searches through their belongings, taking a quick account of their cash.", exclude=self.caller)

class CmdPocket(BaseCommand):
    """
    Pocket a money-object into your wallet. 

    Usage:
          pocket (money object)
    """
    key = 'eat'
        
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

class CurrencyCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCurrency())
        self.add(CmdPocket())