# Part of Shellcuts by Tgsachse.

# File path constants.
F_BASHMARKS=~/.config/shellcuts/zsh/bashmarks-aliases.sh

# Core function of program. Sends first two arguments to sc-handler.
# sc-handler returns a function, which is then executed.
function sc {
    eval "$(python3 /usr/bin/sc-handler $1 $2)"
}

# Full-name aliases.
alias shellcut="sc"
alias shellcuts="sc"
alias shellc="sc"
alias scut="sc"

# If Bashmarks syntax is enabled (e.g. the file exists), load it.
if [ -f "$F_BASHMARKS" ]; then
    . $F_BASHMARKS
fi
