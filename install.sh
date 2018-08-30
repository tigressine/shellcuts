
function append_controller {
    if [ -f $1 ]
    then
        echo "file"
        if [ "$(grep -c -f $2 $1)" -eq 0 ]
        then
            echo "here"
            cat $2 >> $1
        fi
    fi
}

append_controller gooble.txt gerber.txt
