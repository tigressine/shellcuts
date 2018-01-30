# Part of Shellcuts by Tgsachse.

# File path constants.
F_FUNCT=~/.config/shellcuts/zsh/main-function.sh
F_BASHMARKS=~/.config/shellcuts/zsh/bashmarks-aliases.sh

# If main function file exists, load it.
if [ -f "$F_FUNCT" ]; then
    . $F_FUNCT
fi

# If Bashmarks syntax is enabled (e.g. the file exists), load it.
if [ -f "$F_BASHMARKS" ]; then
    . $F_BASHMARKS
fi
