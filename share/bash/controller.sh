# Part of Shellcuts by Tgsachse.

# Absolute location of the plugins folder.
#PLUGINS="$HOME/.config/shellcuts/bash/plugins"
PLUGINS="$HOME/Dropbox/Code/Shellcuts/share/bash/plugins"

# Core function of program. Sends first two arguments to sc-handler.
# sc-handler returns a function, which is then executed.
function sc {
    eval "$(python3 /usr/bin/sc-handler $1 $2)"
}

# Sources all files located in the plugins folder.
for FILE in $PLUGINS/* ; do
    . $FILE
done
