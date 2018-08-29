# Part of Shellcuts by Tgsachse.

HANDLER="~/.shellcuts/binary/shellcuts.pyc"
PLUGINS="~/.shellcuts/config/zsh/plugins/*"

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc {
    eval "$(python3 $HANDLER $1 $2)"
}

# Load all shell plugins.
for FILE in $PLUGINS; do
    . $FILE
done
