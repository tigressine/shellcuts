# FIX DOCUMENTATION

# Core function of program. Sends first two arguments to sc-handler.
# The resulting output determines if the script prints an error message,
# exits quietly, or changes the user's directory.
function sc {
    OUTCOME="$(sc-handler $1 $2)"
    
    if [ "${OUTCOME:0:5}" == "PRINT" ]; then
        echo "${OUTCOME:6:${#OUTCOME}}"
    elif [ "${OUTCOME:0:9}" == "TERMINATE" ]; then
        :
    elif [ "${OUTCOME:0:3}" == "CMD" ]; then
        ${OUTCOME:4:${#OUTCOME}}
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
