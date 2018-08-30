from pathlib import Path
from utilities.commander import Commander
from utilities.parser import Parser
from utilities import constants, extras

commander = Commander(constants.VERSION_FILE, constants.SHELLCUTS_FILE)

parser = Parser(commander)
parser.parse_arguments()

if len(parser.unknown) <= 0:
    commander.go(parser.arguments.name)
    exit(0)

parser.add_arguments()
parser.parse_arguments()

if len(parser.unknown) > 0:
    extras.throw_help()
else:
    commander.execute_command(parser.arguments)
