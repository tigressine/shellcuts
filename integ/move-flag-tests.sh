#!/bin/sh

test_move_flag_simple_path() {
  shell="$1"
  func_source="$2"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Save working root and create two different test paths.
  working_root="$(pwd)"
  testing_root="/tmp/shellcuts-integ-test-$(date +"%s")"
  first_relative_path="a/b/c"
  second_relative_path="d/e/f"
  mkdir -p "$testing_root/$first_relative_path"
  mkdir -p "$testing_root/$second_relative_path"

  # Create a shellcut at the bottom of the first path within the testing root
  # using the specified shell.
  cd "$testing_root/$first_relative_path"
  result="$("$shell" -c ". $func_source; sc -n integ")"
  cd "$working_root"
  if [ "$result" != 'new shellcut "integ" created' ]; then
    printf "shellcut could not be created"
    return 1
  fi

  # Move the shellcut to the second path.
  cd "$testing_root/$second_relative_path"
  result="$("$shell" -c ". $func_source; sc -m integ")"
  cd "$working_root"
  if [ "$result" != 'shellcut "integ" moved' ]; then
    printf "shellcut could not be moved"
    return 1
  fi

  # Jump with the previously-created shellcut to the second path and check that
  # the jump succeeds.
  result="$("$shell" -c ". $func_source; sc integ; pwd")"
  if [ "$result" = "$testing_root/$second_relative_path" ]; then
    return 0
  else
    printf "shellcut did not jump to the expected directory"
    return 1
  fi
}

script_root="$(dirname "$(readlink -fm "$0")")"
shell="$1"
func_source="$2"

# Source the utility functions.
. "$script_root/utils.sh"

# Execute all tests.
run_tests \
  "--move" \
  "$shell" \
  "$func_source" \
  test_move_flag_simple_path
