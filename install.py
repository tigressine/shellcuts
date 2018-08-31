"""
"""
import re
import shutil
import compileall
from pathlib import Path

CORE = 'core'
CACHE = '__pycache__'
SHELLS = ('zsh', 'fish', 'bash')
SOURCE_DIRS = ('docs', 'source', 'shells')
COMPILE_PATTERN = r'^(?P<name>[_a-z]+)\.[\-a-z0-9]+\.pyc$'

DESTINATION_DIRS = {
    'shellcuts' : Path('~/.shellcuts').expanduser(),
    'docs' : Path('~/.shellcuts/docs').expanduser(),
    'data' : Path('~/.shellcuts/data').expanduser(),
    'shells' : Path('~/.shellcuts/shells').expanduser(),
    'source' : Path('~/.shellcuts/source').expanduser(),
    'binaries' : Path('~/.shellcuts/binaries').expanduser(),
    'core' : Path('~/.shellcuts/binaries/core').expanduser(),
}

shutil.rmtree(str(DESTINATION_DIRS['shellcuts']))

DESTINATION_DIRS['shellcuts'].mkdir(parents=True)
for directory in SOURCE_DIRS:
    shutil.copytree(Path(directory), DESTINATION_DIRS[directory])

for directory in DESTINATION_DIRS.keys():
    DESTINATION_DIRS[directory].mkdir(exist_ok=True)

compileall.compile_dir(str(DESTINATION_DIRS['source']))

top_cache = DESTINATION_DIRS['source'] / CACHE
for binary in top_cache.iterdir():
    binary_match = re.match(COMPILE_PATTERN, binary.name)
    target = Path(binary_match.group('name') + '.pyc')
    binary.replace(DESTINATION_DIRS['binaries'] / target)
top_cache.rmdir()

core_cache = DESTINATION_DIRS['source'] / CORE / CACHE
for binary in core_cache.iterdir():
    binary_match = re.match(COMPILE_PATTERN, binary.name)
    target = Path(binary_match.group('name') + '.pyc')
    binary.replace(DESTINATION_DIRS['binaries'] / CORE / target)
core_cache.rmdir()
    
