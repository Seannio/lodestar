class ConsumableObject(DefaultObject):
       # A basic object that can be eaten/drank/smoked/etc. 

       one_consume_only = True
       def at_object_creation(self):
        
           print("wow")

class ConsumableCmdSet(CmdSet):
    def at_cmdset_creation(self):
        print("wow")
        # self.add(CmdBuy())

class CmdEat(Command):
    """
    Usage: 
        eat <thing>
        allows you to eat a consumable object! 
    """
    key = 'eat'
    def func(self):
        if not self.args:
            self.msg("Usage: eat <edible thing>")
            return

        toeat = self.args.strip()
        target = self.caller.search(toeat, candidates=self.caller.contents, typeclass=ConsumableObject)
        if not target: 
            self.msg("You don't have anything by that name.")
            return

        if len(target):
            target = target[0]
        if target.location == self.caller:
                self.caller.msg(f"You eat {target.name}.")
                self.caller.msg_contents(f"{self.caller.name} eats {target.name}.", exclude=self.caller)
                target.delete()



# self.search(query, candidates=self.caller.contents)