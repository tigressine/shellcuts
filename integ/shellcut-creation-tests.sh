#!/bin/sh

# Create a path, create a shellcut for that path, and use that shellcut to jump
# to that path.
_test_shellcut_creation() {
  shell="$1"
  func_source="$2"
  relative_path="$3"

  # Remove the Shellcuts configuration file if it exists.
  rm -f "$HOME/.shellcuts"

  # Save working root and create testing root.
  working_root="$(pwd)"
  testing_root="/tmp/shellcuts-integ-test-$(date +"%s")"
  mkdir -p "$testing_root/$relative_path"
  cd "$testing_root/$relative_path"

  # Create a shellcut at the bottom of the relative path within the testing
  # root using the specified shell, then jump back to the working root.
  first_result="$("$shell" -c ". $func_source; sc -n integ-test")"
  cd "$working_root"
  if [ "$first_result" != 'new shellcut "integ-test" created' ]; then
    printf "shellcut could not be created"
    return 1
  fi

  # Jump with the previously-created shellcut and check that the jump succeeds.
  second_result="$("$shell" -c ". $func_source; sc integ-test; pwd")"
  if [ "$second_result" = "$testing_root/$relative_path" ]; then
    return 0
  else
    printf "shellcut did not jump to the expected directory"
    return 1
  fi
}

test_shellcut_creation_simple_path() {
  _test_shellcut_creation "$1" "$2" "a/B_c/1-2/3"
}

test_shellcut_creation_path_with_spaces() {
  _test_shellcut_creation "$1" "$2" "a/b c d/e f"
}

test_shellcut_creation_path_with_special_characters() {
  _test_shellcut_creation "$1" "$2" 'a/!@#$%/^&*()/+=[]{/}|\~`/"'\''?<>/,.'
}

test_shellcut_creation_path_with_unicode() {
  _test_shellcut_creation "$1" "$2" "a/😀"
}

script_root="$(dirname "$(readlink -fm "$0")")"
shell="$1"
func_source="$2"

# Source the utility functions.
. "$script_root/utils.sh"

# Execute all tests.
run_tests \
  "$shell" \
  "$func_source" \
  test_shellcut_creation_simple_path \
  test_shellcut_creation_path_with_spaces \
  test_shellcut_creation_path_with_special_characters \
  test_shellcut_creation_path_with_unicode
