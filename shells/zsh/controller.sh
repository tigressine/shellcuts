# Part of Shellcuts by Tgsachse.

HANDLER_PATH=~/.shellcuts/binary/sc_handler
PLUGINS_PATH=~/.shellcuts/shells/bash/plugins

# Get a command from the handler, based on the given
# inputs, then execute that command.
function sc {
    eval "$(python3 $HANDLER_PATH $1 $2)"
}

# Load all shell plugins.
for FILE in ${PLUGINS_PATH}/*; do
    . $FILE
done
