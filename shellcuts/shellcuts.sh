# Core function of program. Sends first two arguments to sc-handler.
# The resulting output determines if the script prints an error message,
# exits quietly, or changes the user's directory.
function sc {
    OUTCOME="$(sc-handler $1 $2)"

    if [ "$OUTCOME{:0:5}" == "ERROR" ]; then
        echo "$OUTCOME"
    elif [ "$OUTCOME{:0:10}" == "TERMINATED" ]; then
        exit
    else
        cd $OUTCOME
    fi
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
