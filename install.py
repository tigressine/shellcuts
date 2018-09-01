"""Local installation script for Shellcuts.

This script should work to install Shellcuts on any system with a Unix-like
file organization scheme (e.g. Linux and macOS).

Part of Shellcuts by Tiger Sachse.
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

# add a thing to confirm that all the files exist

# If a shellcuts JSON file already exists, temporarily move it to save it.
if SHELLCUTS_JSON.exists():
    SHELLCUTS_JSON.replace(TEMPORARY_JSON)

# Remove any old installation files.
shutil.rmtree(str(DESTINATION_DIRS['shellcuts']))

# Copy the source directories to the installation location.
DESTINATION_DIRS['shellcuts'].mkdir(parents=True)
for directory in SOURCE_DIRS:
    shutil.copytree(Path(directory), DESTINATION_DIRS[directory])

# Create other destination-only directories that will be used later.
for directory in DESTINATION_DIRS.keys():
    DESTINATION_DIRS[directory].mkdir(exist_ok=True)

# Compile all of the installed source code.
compileall.compile_dir(str(DESTINATION_DIRS['source']))

# Move all compiled top-level files into the binaries folder, then delete the
# compilation cache.
top_cache = DESTINATION_DIRS['source'] / CACHE
for binary in top_cache.iterdir():
    binary_match = re.match(COMPILE_PATTERN, binary.name)
    target = Path(binary_match.group('name') + '.pyc')
    binary.replace(DESTINATION_DIRS['binaries'] / target)
top_cache.rmdir()

# Move all compiled core package files into the binaries/core folder, then
# delete the compilation cache.
core_cache = DESTINATION_DIRS['source'] / CORE / CACHE
for binary in core_cache.iterdir():
    binary_match = re.match(COMPILE_PATTERN, binary.name)
    target = Path(binary_match.group('name') + '.pyc')
    binary.replace(DESTINATION_DIRS['binaries'] / CORE / target)
core_cache.rmdir()

# Append example shell configuration instructions to existing shell
# configuration files. These configuration instructions allow Shellcuts to
# hook into the shell correctly.
for shell in SHELLS:

    # Only append to configuration files that exist.
    if SHELL_CONFIGS[shell].exists():
        with open(SHELL_EXAMPLES[shell], 'r') as f:
            new_lines = f.readlines()

        with open(SHELL_CONFIGS[shell], 'r') as f:
            shell_lines = f.readlines()

            # If the current configuration file already has the necessary
            # instructions (from a previous install) then don't add them again.
            for new_line in new_lines:
                if new_line not in shell_lines:
                    missing_new_lines = True
                    break
            else:
                missing_new_lines = False

        # if the instructions are not in the configuration file, add them.
        if missing_new_lines:
            with open(SHELL_CONFIGS[shell], 'a') as f:
                for new_line in new_lines:
                    f.write(new_line)

# Move the old shellcuts JSON back into place.
if TEMPORARY_JSON.exists():
    TEMPORARY_JSON.replace(SHELLCUTS_JSON)
