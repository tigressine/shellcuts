# Process arguments with sc-core, then evaluate the result as a shell command.
sc() {
  eval "$(sc-core "$@")"
}
