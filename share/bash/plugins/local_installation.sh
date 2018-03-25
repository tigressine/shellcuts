# Part of Shellcuts by Tgsachse.

# Overrides sc function defined in controller.sh to instead call a
# locally installed version of the sc-handler script.
function sc {
    eval "$(python3 $HOME/.shellcuts/bin/sc-handler $1 $2)"
}
