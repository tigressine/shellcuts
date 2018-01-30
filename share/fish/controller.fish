# Part of Shellcuts by Tgsachse.

# File path constants.
set F_FUNCT ~/.config/shellcuts/fish/main-function.fish
set F_BASHMARKS ~/.config/shellcuts/fish/bashmarks-aliases.fish

# If main function file exists, load it.
if test -e $F_FUNCT
    . $F_FUNCT
end

# If Bashmarks syntax is enabled (e.g. the file exists), load it.
if test -e $F_BASHMARKS
    . $F_BASHMARKS
end
