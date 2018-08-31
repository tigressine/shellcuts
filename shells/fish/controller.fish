# Part of Shellcuts by Tgsachse.

set SHELLCUTS_HANDLER "~/.shellcuts/binaries/shellcuts.pyc"
set SHELLCUTS_PLUGINS "~/.shellcuts/shells/fish/plugins/*"

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc
    set -l IFS
    eval (python3 $SHELLCUTS_HANDLER $argv)
    set -e IFS
end

# Load all shell plugins.
for FILE in $SHELLCUTS_PLUGINS
    . $FILE
end
