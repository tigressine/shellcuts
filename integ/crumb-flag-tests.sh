#!/bin/sh

# Create a path, create a crumb at that, and use that crumb to jump back to
# that path.
_test_crumb_flag() {
  shell="$1"
  func_source="$2"
  relative_path="$3"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Save working root and create testing root.
  working_root="$(pwd)"
  testing_root="/tmp/shellcuts-integ-test-$(date +"%s")"
  mkdir -p "$testing_root/$relative_path"

  # Create a crumb at the bottom of the relative path within the testing root
  # using the specified shell, then jump back to the working root.
  cd "$testing_root/$relative_path"
  result="$("$shell" -c ". $func_source; sc -c")"
  cd "$working_root"
  if [ "$result" != 'crumb added for this location' ]; then
    printf "crumb could not be created"
    return 1
  fi

  # Jump to the crumb and check that the jump succeeds.
  result="$("$shell" -c ". $func_source; sc; pwd")"
  if [ "$result" = "$testing_root/$relative_path" ]; then
    return 0
  else
    printf "shellcut did not jump to the expected directory"
    return 1
  fi
}

test_crumb_flag_simple_path() {
  _test_crumb_flag "$1" "$2" "a/B_c/1-2/3"
}

test_crumb_flag_path_with_spaces() {
  _test_crumb_flag "$1" "$2" "a/b c d/e f"
}

test_crumb_flag_path_with_special_characters() {
  _test_crumb_flag "$1" "$2" 'a/!@#$%/^&*()/+=[]{/}|\~`/"'\''?<>/,.'
}

test_crumb_flag_path_with_unicode() {
  _test_crumb_flag "$1" "$2" "a/😀"
}

script_root="$(dirname "$(readlink -fm "$0")")"
shell="$1"
func_source="$2"

# Source the utility functions.
. "$script_root/utils.sh"

# Execute all tests.
run_tests \
  "--crumb" \
  "$shell" \
  "$func_source" \
  test_crumb_flag_simple_path \
  test_crumb_flag_path_with_spaces \
  test_crumb_flag_path_with_special_characters \
  test_crumb_flag_path_with_unicode
