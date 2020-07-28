# Process arguments with sc-core, then evaluate the result as a shell command.
function sc
  set -l IFS
  eval (sc-core $argv)
  set -e IFS
end
