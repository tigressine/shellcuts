from core.database import DatabaseConnection
from core.parser import Parser
from core.commands import *

parser = Parser()
arguments, unknown = parser.parse_known_args()

# Attempts to short-circuit the program and jump if only one argument given.
if len(unknown) < 1:
    command_go(arguments.shellcut)
    exit(0)

# Adds other flags and re-parses arguments.
parser.add_additional_arguments()
arguments, unknown = parser.parse_known_args()

# If anything unknown is passed, show help and exit.
if len(unknown) > 0:
    command_help()
    exit(0)

# This tuple associates arguments from the parser with their functions.
command_pairs = ( # there's gotta be abetter way
    (arguments.help, command_help),
    (arguments.list, command_list),
    (arguments.version, command_version),
    (arguments.init, command_init),
    (arguments.bashmarks, command_bashmarks),
    (arguments.delete, command_delete),
    (arguments.new, command_new),
    (arguments.move, command_move),
    (arguments.print, command_print))

# For each in tuple, if value is not 'None', execute associated function.
for pair in command_pairs:
    if pair[0] != None:
        # Passes value to corresponding function. Functions are designed to
        # handle this value even if they don't need it.
        pair[1](pair[0])
        break
else:
    command_help()
