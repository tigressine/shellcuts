# Part of Shellcuts by Tgsachse.

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc {
    eval "$(python3 $HOME/.shellcuts/binaries/shellcuts.pyc $1 $2)"
}

# Load all shell plugins.
for FILE in $HOME/.shellcuts/shells/bash/plugins/*; do
    . $FILE
done
