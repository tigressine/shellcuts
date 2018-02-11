# Part of Shellcuts by Tgsachse.

# Core function of program. Sends first two arguments to sc-handler.
# sc-handler returns a function, which is then executed.
function sc {
    eval "$(python3 sc-handler $1 $2)"
}

# Full-name aliases.
alias shellcut="sc"
alias shellcuts="sc"
alias shellc="sc"
alias scut="sc"
