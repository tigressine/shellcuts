# Part of Shellcuts by Tgsachse.

F_FUNCT="~/.config/shellcuts/bash/main-function.sh"
F_BASHMARKS="~/.config/shellcuts/bash/bashmarks-aliases.sh"

# If main function file exists, load it.
if [ -f $F_FUNCT ]; then
    . $F_FUNCT
fi

# If Bashmarks syntax is enabled (e.g. the file exists), load it.
if [ -f $F_BASHMARKS ]; then
    . $F_BASHMARKS
fi
