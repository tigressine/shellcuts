# Part of Shellcuts by Tgsachse.

# File path constants.
set F_BASHMARKS ~/.config/shellcuts/fish/bashmarks-aliases.fish

# Core function of program. Sends first two arguments to sc-handler.
# sc-handler returns a function, which is then executed.
function sc
    set -l IFS
    eval (python3 /usr/bin/sc-handler $argv)
    set -e IFS
end

# Full-name aliases.
alias shellcut="sc"
alias shellcuts="sc"
alias shellc="sc"
alias scut="sc"

# If Bashmarks syntax is enabled (e.g. the file exists), load it.
if test -e $F_BASHMARKS
    . $F_BASHMARKS
end
