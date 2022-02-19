from room import Room
from items import Items
from command_parser import Parser
from command import Command

"""
 *  This class is the main class of the Pirate game application. 
 *  this is a very simple, text based adventure game.  Users 
 *  can walk around some scenery. That's all. It should really be extended 
 *  to make it more interesting!
 * 
 *  To play this game, create an instance of this class and call the "play"
 *  method.
 * 
 *  This main class creates and initialises all the others: it creates all
 *  rooms, creates the parser and starts the game.  It also evaluates and
 *  executes the commands that the parser returns.
"""

class Game():
    """ To play this game, create an instance of this class and call the "play"  method.
    This main class creates and initialises all the others: it creates all
    rooms, creates the parser and starts the game.  It also evaluates and
    executes the commands that the parser returns.
    """
    def __init__(self):
        """ Create the game and initialise its internal map. """ 
        # Allow for items, inventory and process flags for changes in goals
        self.all_items = Items()
        self.create_items()
        self.create_rooms()
        self.parser = Parser()
        self.inventory = {}
        self.initial_conversation_done = False
        self.completed_game = False

    def create_rooms(self):
        """ Create all the rooms and link their exits together. """
        # create the rooms and their discriptions to print when the play enters the room
        dock = Room("standing on the wooden docks.\nYour sloop and a huge galleon are attached.\nThe town is to the east", "dock")
        sloop = Room("on your modest sloop, it use to belong to your grandfather.\nYou can't sail it without a 'Pirate's license' though", "sloop")
        galleon = Room("stepping onto the galleon when a voice shouts down at you from the deck of the ship\n'ARH! GET YER DIRTY HANDS OFF MY SHIP!'\nIt's probably best to leave..", "galleon")
        town = Room("in the town center, it looks run down and rough.\nYou can see a dark jungle to the north of the town.\nA sandy path to the south looks like it leads to a beach.\nYou can see the masts of ships to the west.\nThere's alot of noise coming from a pub to the east", "town")
        pub = Room("in the Hound Pits Pub, it smells like a mixture of smoke and sweat.\nThe pub is crowded by men singing and drinking to some sort of sea shanty... You've never heard it before.\nThere's a strange smell coming from the kitchen to the east.\nYou notice a staircase heading downwards to the south", "pub")
        kitchen = Room("in the kitchen of the pub, it looks like it has seen better days.\nYou notice the smell is coming from a liquid bubbling away in a pot over a fire.\nIt doesn't look it would be edible..", "kitchen")
        viproom = Room("following the staircase down until you reach a quite room.\nThree captians are sat at a table.\nThey look up from their card game to glare at you before returning their attention back to the cards.\nOne of the captains has an eyepatch, the second has a wooden leg and the third has a hook replacing his hand", "viproom")
        beach = Room("walking down the sandy path until you reach a picturesque beach.\nThe smell of the salty air and the sound of the waves crashing on the shore calms you.\nYou can just make out what looks like a ship on the shore to the east", "beach")
        shipwreak = Room("near a shipwreak that has washed up on the beach.\nIt looks like it has been here a long time.\nYou notice the large bite taken out of the ship's stern and recall the stories your grandfather use to tell you of sea-monsters and krakens", "shipwreck")
        jungle = Room("in the jungle, it's so dark that you can't see anything and keep tripping on the roots of the trees.\nYou notice a faint light coming from the north.\nYou can also see a large stone fort towards the east of the jungle", "jungle")
        fort = Room("in an stone fort, it looks like it's from a war that ended many years ago.\nThere are rusty cannons looking over the fort's walls towards the sea.\nYou notice a stairwell to the east leading to the dark", "fort")
        dungeon = Room("slowly climbing down the stairs, the stone walls feel cold and slimy.\nYou finally reach a room lit by a single torch and duck your head under the chains hanging from the ceiling.\nAt the back of the room is an iron cage with the remains of a skeleton lying inside.\nYou feel like something is breathing down your neck..", "dungeon")
        campsite = Room("following the light until you reach a clearing in the jungle.\nTwo men are sat next to a campfire. They are handing a bottle of something back and forth between one another.\nOne of them nods for you to join them and the other hands you the bottle.\nYou take a swig and hand it to the next man... it taste fowl", "campsite")

        # initialise room exits and item placements
        dock.set_exit("east", town)
        dock.set_exit("south", sloop)
        dock.set_exit("north", galleon)
        # print(dock.get_item("key")) #used in testing item

        sloop.set_exit("north", dock)

        galleon.set_exit("south", dock)

        town.set_exit("west", dock)
        town.set_exit("east", pub)
        town.set_exit("north", jungle)
        town.set_exit("south", beach)

        pub.set_exit("west", town)
        pub.set_exit("east", kitchen)
        pub.set_exit("south", viproom)

        kitchen.set_exit("west", pub)
        kitchen.set_item("grog", self.all_items.get_item_description("grog"))
        
        viproom.set_exit("north", pub)

        beach.set_exit("north", town)
        beach.set_exit("east", shipwreak)

        shipwreak.set_exit("west", beach)
        shipwreak.set_item("compass", self.all_items.get_item_description("compass"))

        jungle.set_exit("south", town)
        jungle.set_exit("north", campsite)
        jungle.set_exit("east", fort)

        campsite.set_exit("south", jungle)

        fort.set_exit("west", jungle)
        fort.set_exit("east", dungeon)

        dungeon.set_exit("west", fort)
        dungeon.set_item("key", self.all_items.get_item_description("key"))


        self.current_room = dock;  # start game at the dock

    def create_items(self):
        # discriptions of the items
        self.all_items.add_new_item("key", "A key sat in the lock of the iron cage catches your eye.\nMaybe the skeleton is Mad Claw McGree and this is the key one of the captains was asking for.")
        self.all_items.add_new_item("compass", "There's a compass in what used to be the captain's quaters of the ship.\nIt looks very old and rusty.\nMaybe it's the compass that belonged to the missing captain grey beard.")
        self.all_items.add_new_item("grog", "Next to the pot is a pint of grog.\nIt looks and smells the same as the substance in the pot")
        self.all_items.add_new_item("pirate's license", "I finaly got my pirate's license")

    def play(self):
        """ Main play routine.  Loops until end of play """
        self.print_welcome()

        # Enter the main command loop.  Here we repeatedly read commands and
        # execute them until the game is over.
                
        finished = False
        while finished == False:
            if self.completed_game:
                break
            command = self.parser.get_command()
            finished = self.process_command(command)
        print("Thank you for playing.  We hope you enjoyed our game, Sam and Harvey!.")

    def print_welcome(self):
        """ Print out the opening message for the player """
        # establish setting and primary objective
        print()
        print("Welcome to Pirate Island!")
        print("This is it the day you've been waiting your whole life for.\nTo finally follow your grandfather's footsteps and set sail on your own pirate adventure.")
        print("Unfortunately, just as you're about to hoist your sloop's sail a man grabs you by the arm and asks")
        print("'Arh! Have ye got yer pirate's license?'")
        print("'Pirate's license?' you reply.")
        print("'Arh! Can't let ye set sail without one!' he barks")
        print("'If ye don't have one, one of the captains will be able to give ye one. Ye'll probably find them in the pub to the east at this time of night.'")
        print("'Okay... thanks.' you say as you step off the deck of your ship onto the wooden dock.")
        print("'Arh! Good luck to ye.' he says as he walks off to check someone else for their license.")
        print()
        print("Type 'help' if you need help.")
        print()
        print(self.current_room.get_long_description())

    def process_command(self, command):
        """ Given a command, process (that is: execute) the command.

        Parameters
        ----------
        command: Command
            The command to be processed
        
        Returns true If the command ends the game, false otherwise.
        """
        want_to_quit = False

        if command.is_unknown():
            print("I don't know what you mean...")
            return False

        command_word = command.get_command_word()
        # Set the commands the player will type to control the game
        if command_word == "help":
            self.print_help()
        elif command_word == "go":
            self.go_room(command)
        elif command_word == "quit":
            want_to_quit = self.quit(command)
        elif command_word == "get":
            self.get_item(command)
        elif command_word == "inventory":
            self.print_inventory()
        elif command_word == "talk":
            self.talk()
        
        return want_to_quit

    # implementations of user commands:

    def print_help(self):
        """ Print out some help information. """
        # Shows the current objective and changes it due to the state of the players inventory and whether they've reach a progression check  
        print("You Need to get your 'pirate's license'.")

        if "pirate's license" in self.inventory:
            # Final objective
            print("Go back to your ship to start your pirate adventure!")
        elif "key" in self.inventory and "compass" in self.inventory and "grog" in self.inventory:
            # Gathered all items
            print("Talk to the captains to give them their requested items in exchange for a pirate's license.")
        elif self.initial_conversation_done:
            # Progress flag
            print("You need to find the items that the captians asked you to fetch.")
        else:
            # First objective
            print("The man at the dock said to talk to the captains in the pub to the east of town.")
        print()
        print("Your command words are:")
        self.parser.show_commands()

    def print_inventory(self):
        # Allows the player to see what items they have
        return_string = "You currently have:"
        if len(self.inventory) == 0:
            return_string += " nothing"
        else:
            for item_name in self.inventory.keys():
                return_string += " " + item_name
        print(return_string)

    """
     * Try to in to one direction. If there is an exit, enter the new
     * room, otherwise print an error message.
    """
    def go_room(self, command):
        """ Try to in to one direction. If there is an 3xit, enter the new
        room, otherwise print an error message.

        Parameters
        ----------
        command: Command
            The command to be processed
        """
        if command.has_second_word() == False:
            # if there is no second word, we don't know where to go...
            print("Go where?")
            return

        direction = command.get_second_word()

        # Try to leave current room.
        next_room = self.current_room.get_exit(direction)

        if next_room == None:           # None is a special Python value that says the variable contains nothing
            print("There no where to go that way.")
        else:
            self.current_room = next_room
            if self.current_room.get_name() == "sloop" and "pirate's license" in self.inventory:
                # Game over text here and quits the game
                print("You show the man at the docks you license and jump onto your sloop.")
                print("You can finally hoist your sails and set off on your adventure on the open seas.")
                self.completed_game = True
                #self.process_command(Command("quit", None)) # Doesn't work
            else:
                print(self.current_room.get_long_description())

    def get_item(self,command):
        if command.has_second_word == False:
            print("Get what?")
            return

        item = command.get_second_word()
        # Double check to make sure we don't already have this item in our inventory
        # shows error message
        if item in self.inventory:
            print("You already have that item.")
        else:
            if self.all_items.get_item_exists(item):
                self.inventory[item] = self.all_items.get_item_description(item)
                print("You pick up the " + item)
                self.current_room.remove_item(item)
            else:
                print("There is no " + item)

    def talk(self):
        # Function to allow the player to talk

        # Talking to people in the viproom
        if self.current_room.get_name() == "viproom":
            # Checks if the player has got all the items required, if so prints text, deletes items from inventory and adds new item to inventory 
            if self.initial_conversation_done:
                if "key" in self.inventory and "compass" in self.inventory and "grog" in self.inventory:
                    print("'Here's everything you asked for.' you say as you hand out each item.")
                    print("'Arh! About time to!' one of the captains says.\nAnother throws you a piece of paper and says,\n'There's your license, now scram.'")
                    print("The three of them start laughing as you pocket you license.")
                    self.inventory["pirate's license"] = self.all_items.get_item_description("pirate's license")
                    self.inventory.pop("key")
                    self.inventory.pop("compass")
                    self.inventory.pop("grog")
                elif "pirate's license" in self.inventory:
                    print("'Yer got yer pirate's license now get out of here!'")

                else:
                    # If intial conversation flag is checked but not all items are in inventory it will diplay this text
                    print("'Arh! You have all the stuff we ask for yet... No! then stop bothering us!'")
                    print("'Remeber, we want a compass, a key and a...'")
                    print("'A PINT OF GROG!'")
            else:
                # Flavour text to establish second objective (i.e. fetch quest) sets the progress flag as true to change the help function and captians' text
                print("'Urmm hello?' you say")
                print("'What do yer want?' one of the captains asks without looking away from his cards.")
                print("'I need a pirate's lisence and was told you may be able to give me one' you answer.")
                print("'Arh but we ain't going to just give yer one. You have to earn it' another captian says")
                print("'Arh! That's right.' the third captain says, 'why dont you go get me the lost compass of the great captian grey beard.'")
                print("'I'll need the key that locked Mad Claw McGree up.' another captain says while picking his nose with his hock hand.")
                print("'And I just want a pint of grog... I'm thirsty yer see.' he has still not looked away from his cards.")
                print("'Right, so I need to get; a compass, a key and a pint of grog?' You ask.")
                print("'Arh! Now go leave us alone will ya!'")
                self.initial_conversation_done = True
        elif self.current_room.get_name() == "campsite":
            # Talk text to change on the current room for the rest of the map
            print("You greet the two men but they don't say anything in return.\nThey don't seem to be very talkative.")
        elif self.current_room.get_name() == "dock" or self.current_room.get_name() == "town" or self.current_room.get_name() == "pub" or self.current_room.get_name() == "galleon":
            print("No one is here wants to talk to you.")
        else:
            print("There is no one here to talk to you.")

    def quit(self, command):
        """ "Quit" was entered. Check the rest of the command to see whether we really quit the game.

        Parameters
        ----------
        command: Command
            The command to be processed
        
        Returns true, if this command quits the game, false otherwise.
        """
        if command.has_second_word():
            print("Quit what?")
            return False
        else: 
            return True  # Signal that we want to quit
