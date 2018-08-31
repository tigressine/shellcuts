"""
"""
from core import utilities
from core.parser import Parser
from core.commander import Commander

commander = Commander(utilities.VERSION_FILE,
                      utilities.SHELLCUTS_FILE,
                      utilities.MANUAL_FILE)

parser = Parser(commander)
parser.parse_arguments()

if parser.arguments.name is None:
    utilities.throw_help()
elif len(parser.unknown) <= 0:
    commander.go(parser.arguments.name)
    exit(0)

parser.add_arguments()
parser.parse_arguments()

if len(parser.unknown) > 0:
    utilities.throw_help()
else:
    commander.execute(parser.arguments)
