"""Main driver and entry point for Shellcuts.

This script parses command line arguments and ultimately prints a shell command
to stdout. It is only ever called by a shell script that captures the printed
shell command and evaluates it.

Part of Shellcuts by Tiger Sachse.
"""
from core import utilities
from core.parser import Parser
from core.commander import Commander

commander = Commander(utilities.VERSION_FILE,
                      utilities.SHELLCUTS_FILE,
                      utilities.MANUAL_FILE)

# The initial parser only accepts 'go' commands (in an attempt to
# short-circuit the program). This allows the most common command to execute
# as quickly as possible.
parser = Parser()
parser.parse_arguments()

# If there are no unknowns after the initial parse then it must
# be a 'go' command.
if len(parser.unknown) <= 0:
    commander.go(parser.arguments.name)
    exit(0)

# Add in all the rest of the arguments and re-parse.
parser.add_arguments()
parser.parse_arguments()

# Unknowns trigger the help menu, else tell the commander to execute.
if len(parser.unknown) > 0:
    utilities.throw_help()
else:
    commander.execute(parser.arguments)
