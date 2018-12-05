# Part of Shellcuts by Tgsachse.

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc {
    eval "$(python3 $HOME/.shellcuts/binaries/shellcuts.pyc "$@")"
}

# Load all shell plugins.
for FILE in $HOME/.shellcuts/shells/ksh/plugins/*; do
    . $FILE
done
