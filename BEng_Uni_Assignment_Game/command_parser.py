from command import Command
from command_words import CommandWords

class Parser():
    """
     This parser reads user input and tries to interpret it as an "Adventure"
     command. Every time it is called it reads a line from the terminal and
     tries to interpret the line as a two word command. It returns the command
     as an object of class Command.

     The parser has a set of known command words. It checks user input against
     the known commands, and if the input is not one of the known commands, it
     returns a command object that is marked as an unknown command.
    """
    def __init__(self):
        """ Create a parser to read from the terminal window """
        self.commands = CommandWords()

    def get_command(self):
        """ Returns The next command from the user """
        
        # Initialise word1 and word2 to <None>
        word1 = None        # None is a special Python value that says the variable contains nothing
        word2 = None

        input_line = input( "> " )

        # Find up to two words on the line and set word1 and word2 appropriately
        tokens = input_line.strip().split( " " )
        if len( tokens ) > 0:
            word1 = tokens[0]
            if len( tokens ) > 1:
                word2 = tokens[1]

        # Now check whether this word is known. If so, create a command
        # with it. If not, create a <None> command (for unknown command).
        if(self.commands.is_command(word1)):
            return Command(word1, word2)
        else:
            return Command(None, word2); 

    def show_commands(self):
        """ Print out a list of valid command words. """
        self.commands.show_all()
