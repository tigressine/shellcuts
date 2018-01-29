# Part of Shellcuts by Tgsachse.

# Core function of program. Sends first two arguments to sc-handler.
# sc-handler returns a function, which is then executed.
function sc {
    eval "$(sc-handler $1 $2)"
}

# Aliases to make use of this program more familiar. Can be broken down
# into two catagories: short-hand/long-hand and original syntax from huyng/bashmarks.
# These first aliases are short-hand/long-hand.
alias shellcut="sc"
alias shellcuts="sc"
alias shellc="sc"
alias scut="sc"

# These aliases are meant to emulate the original huyng/bashmarks syntax.
alias s="sc -n"
alias g="sc"
alias p="sc -p"
alias d="sc -d"
alias l="sc -l"
