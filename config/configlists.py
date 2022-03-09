
SCREENOBJECT_STRINGS = (
                "\nOn the tiny holopanel: An ad for Astro Lite, the universe's favorite lager brewed in space!",
                "\nOn the tiny holopanel: A technicolor ad for the wonders of flesh-eating nanites. ",
                "\nOn the tiny holopanel: A dead rat spinning perpetually.",
                "\nOn the tiny holopanel: A hat with fuzzy legs dancing to some out-of-date polka.",
                "\nOn the tiny holopanel: A static picture of a frog with six eyes, imploring you to invest in a company named TOADLICK.",
                "\nOn the tiny holopanel: A breakdancing piece of toast with a jingle that you can barely hear.",
                "\nOn the tiny holopanel: A series of graphs explaining interstellar economy. Boring.",
                "\nOn the tiny holopanel: A space-drama dubbed in neo-italian, with lips that don't match up to the words."
)

CONSUMABLE_MESSAGE_TYPES = ('con_msg',
                            'ocon_msg',
                            'finish_msg',
                            'ofinish_msg,'
                            'chug_msg', 
                            'ochug_msg'
)

CONSUMABLE_DRUG_MESSAGES = ( 'You feel a rusty taste on the back of your tongue, like you\'ve been licking old plumbing',
                             'The world feels like an awful, sweaty place, prickling hotly across your skin.'

)

FURNITURE_MESSAGE_TYPES = (
                            'sit_msg',
                            'osit_msg',
                            'stand_msg',
                            'ostand_msg',
                            'seat_pose'
)

randomgoods = (
                "|ySandmelt Vibrofruit Martini|n",
                "|wWhite Ruskovian|n",
                "|YGolden Stopwatch cocktail|n",
                "|!RTwelve-Mango Special|n",
                "|CMageweaver's Menta|n",
                "|yBrewer's Pudding|n",
                "|gBackalley Bog Grog|n",
                "|mGrenadine Spritz|n",
                "|xLey-Vodka Sour|n",
                "|gSpicy Cactus-Jack|n",
                "|xSmoke-Rakja Highball|n",
                "|rFlaming Bushwrangler|n" 
)

randomcups = ( 
                "crystalline martini glass",
                "tall flute-glass",
                "engraved, old-fashioned glass",
                "simple crystal shot-glass",
                "crystalline highball glass",
                "curiously-shaped cocktail glass",
                "shiny, thin-stemmed wineglass"
)

ECHOES = (
                "A bespokely-dressed waiter delicately squeezes through the patrons, carefully carrying two glasses of " + random.choice(randomgoods) + " on a platter.",
                "Over the quiet, ambient music, a touch of conversation picks up at a nearby table, followed by soft laughter.",
                "From the depths of the cosmos beyond the window, hazy heatwaves distort the faraway colours in a momentary ripple.",
                "Behind the bar, a busy clockwork creature whirrs to life, its spindly brass arms collecting the requisite bottles for a " + random.choice(randomgoods) + ".",
                "Behind the bar, a creaky clockwork mixing-figure austerely shakes a drink with mechanical precision. It eventually pours a " + random.choice(randomgoods) + " into a " + random.choice(randomcups)+ ".",
                "Behind the bar, a tired clockwork slicing-machine cuts up a variety of small fruit-pieces, depositing them into a bin for cocktailmaking.",
)
