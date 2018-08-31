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
TEMPORARY_JSON = Path('/tmp/shellcuts.json.temp')
COMPILE_PATTERN = r'^(?P<name>[_a-z]+)\.[\-a-z0-9]+\.pyc$'
SHELLCUTS_JSON = Path('~/.shellcuts/data/shellcuts.json').expanduser()

SHELL_CONFIGS = {
    'zsh' : Path('~/.zshrc').expanduser(),
    'bash' : Path('~/.bashrc').expanduser(),
    'fish' : Path('~/.config/fish/config.fish').expanduser(),
}
SHELL_EXAMPLES = {
    'zsh' : Path('~/.shellcuts/shells/zsh/zshrc.example').expanduser(),
    'bash' : Path('~/.shellcuts/shells/bash/bashrc.example').expanduser(),
    'fish' : Path('~/.shellcuts/shells/fish/config.fish.example').expanduser(),
}
DESTINATION_DIRS = {
    'shellcuts' : Path('~/.shellcuts').expanduser(),
    'docs' : Path('~/.shellcuts/docs').expanduser(),
    'data' : Path('~/.shellcuts/data').expanduser(),
    'shells' : Path('~/.shellcuts/shells').expanduser(),
    'source' : Path('~/.shellcuts/source').expanduser(),
    'binaries' : Path('~/.shellcuts/binaries').expanduser(),
    'core' : Path('~/.shellcuts/binaries/core').expanduser(),
}

# Save any existing json file
if SHELLCUTS_JSON.exists():
    SHELLCUTS_JSON.replace(TEMPORARY_JSON)

# remove old installations
shutil.rmtree(str(DESTINATION_DIRS['shellcuts']))

# copy directories
DESTINATION_DIRS['shellcuts'].mkdir(parents=True)
for directory in SOURCE_DIRS:
    shutil.copytree(Path(directory), DESTINATION_DIRS[directory])

# make any directories we missed in copying
for directory in DESTINATION_DIRS.keys():
    DESTINATION_DIRS[directory].mkdir(exist_ok=True)

# compile everything
compileall.compile_dir(str(DESTINATION_DIRS['source']))

# move bytecode to binaries
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

# add configs as needed.
for shell in SHELLS:
    if SHELL_CONFIGS[shell].exists():
        with open(SHELL_EXAMPLES[shell], 'r') as f:
            new_lines = f.readlines()

        with open(SHELL_CONFIGS[shell], 'r') as f:
            shell_lines = f.readlines()

            for new_line in new_lines:
                if new_line not in shell_lines:
                    missing_new_lines = True
                    break
            else:
                missing_new_lines = False

        print(shell, missing_new_lines)
        if missing_new_lines:
            with open(SHELL_CONFIGS[shell], 'a') as f:
                for new_line in new_lines:
                    f.write(new_line)

# if a temporary file was saved, move
if TEMPORARY_JSON.exists():
    TEMPORARY_JSON.replace(SHELLCUTS_JSON)
