# Part of Shellcuts by Tgsachse.

HANDLER="~/.shellcuts/binaries/shellcuts.pyc"
PLUGINS="~/.shellcuts/shells/bash/plugins/*"

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc {
    eval "$(python3 $HANDLER $1 $2)"
}

# Load all shell plugins.
for FILE in $PLUGINS; do
    . $FILE
done
