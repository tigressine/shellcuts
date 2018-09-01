# Part of Shellcuts by Tgsachse.

# Get a command from the Python handler, based on
# the given inputs, then execute that command.
function sc
    set -l IFS
    eval (python3 $HOME/.shellcuts/binaries/shellcuts.pyc $argv)
    set -e IFS
end

# Load all shell plugins.
for FILE in $HOME/.shellcuts/shells/fish/plugins/*
    . $FILE
end
