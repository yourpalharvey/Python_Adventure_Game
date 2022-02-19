"""
 * Class Room - a room in an adventure game.
 *
 * This class is part of the "World of Zuul" application. 
 * "World of Zuul" is a very simple, text based adventure game.  
 *
 * A "Room" represents one location in the scenery of the game.  It is 
 * connected to other rooms via exits.  For each existing exit, the room 
 * stores a reference to the neighboring room.
 * 
"""

class Room():
    """ A "Room" represents one location in the scenery of the game.  It is 
    connected to other rooms via exits.  For each existing exit, the room 
    stores a reference to the neighboring room.
    """

    def __init__(self, description, name):
        """ Create a room described "description". Initially, it has
        no exits. "description" is something like "a kitchen" or
        "an open court yard".

        Paramaters
        ----------
        description: string
            The room's description
        """
        self.description = description
        self.name = name
        self.exits = {}
        self.items = {}

    def set_exit(self, direction, neighbour):
        """ Define an exit from this room.

        Parameters
        ----------
        direction: string
            The direction of the exit
        neighbour: Room
            The room to which the exit leads
        """
        self.exits[direction] = neighbour

    def set_item(self, item, description):

        self.items[item] = description

    def get_name(self):
        return self.name

    def get_short_description(self):
        """ Returns The short description of the room
        (the one that was defined in the constructor).
        """
        return self.description

    def get_long_description(self):
        """ Return a description of the room in the form:
        You are in the kitchen.
        Exits: north west
        
        Returns A long description of this room
        """
        return "You are " + self.description + ".\n" + self.get_item_string() + self.get_exit_string()

    def get_exit_string(self):
        """ Return a string describing the room's exits, for example
        "Exits: north west".
     
        Returns Details of the room's exits.
        """
        return_string = "Exits:"
        for room_exit in self.exits.keys():
            return_string += " " + room_exit
        return return_string

    def get_item_string(self):
        # Deletes the item discription from the room when it has bee picked up
        return_string = ""
        for item in self.items.keys():
            return_string += self.items.get(item) + "\n"
        return return_string

    """
     * Return the room that is reached if we go from this room in direction
     * "direction". If there is no room in that direction, return None.
     *     direction The exit's direction.
     *     Returns The room in the given direction.
    """
    def get_exit(self, direction):
        """ Return the room that is reached if we go from this room in direction
        "direction". If there is no room in that direction, return None.

        Parameters
        ----------
        direction: string4
            direction The exit's direction.
        
        Returns The room in the given direction.
        """
        if direction in self.exits:
            return self.exits[direction]
        else:
            return None        # None is a special Python value that says the variable contains nothing

    def get_item(self, item):
        #Function to create items
        if item in self.items:
            return self.items[item]
        else:
            return None

    def remove_item(self, item):
        #Function to remove items
        if item in self.items:
            self.items.pop(item)