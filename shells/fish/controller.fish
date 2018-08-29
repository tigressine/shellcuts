# Part of Shellcuts by Tgsachse.

set HANDLER "~/.shellcuts/binaries/shellcuts.pyc"
set PLUGINS "~/.shellcuts/shells/fish/plugins/*"

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc
    set -l IFS
    eval (python3 $HANDLER $argv)
    set -e IFS
end

# Load all shell plugins.
for FILE in $PLUGINS
    . $FILE
end
