# Part of Shellcuts by Tgsachse.

SHELLCUTS_HANDLER="~/.shellcuts/binary/shellcuts.pyc"
SHELLCUTS_PLUGINS="~/.shellcuts/config/zsh/plugins/*"

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc {
    eval "$(python3 $SHELLCUTS_HANDLER $1 $2)"
}

# Load all shell plugins.
for FILE in $SHELLCUTS_PLUGINS; do
    . $FILE
done
