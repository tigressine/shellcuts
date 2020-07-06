# Process arguments with sc-core, then evaluate the result as a shell command.
function sc {
  eval "$(sc-core "$@")"
}
