#!/bin/sh

_test_follow_flag() {
  shell="$1"
  func_source="$2"
  specificity="$3"
  relative_path="$(dirname "$4")"
  test_file="$(basename "$4")"
  command="$5"
  expected_stdout="$6"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Save working root and create testing root.
  working_root="$(pwd)"
  testing_root="/tmp/shellcuts-integ-test-$(date +"%s")"
  rm -rf "$testing_root"
  mkdir -p "$testing_root/$relative_path"
  cd "$testing_root/$relative_path"
  touch "$test_file"

  # Create a shellcut.
  result="$("$shell" -c ". $func_source; sc -n integ")"
  cd "$working_root"
  if [ "$result" != 'new shellcut "integ" created' ]; then
    printf "shellcut could not be created"
    return 1
  fi

  # Ensure that the shellcut is added to the configuration file.
  grep -q "integ" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "shellcut could not be found in the configuration file"
    return 1
  fi

  # Set a follow command for either a specific shellcut or as the default
  # follow command.
  case "$specificity" in
    "shellcut-specific")
      result="$("$shell" -c ". $func_source; sc -f integ '$command'")"
      if [ "$result" != 'follow command updated for shellcut "integ"' ]; then
        printf "follow command was not saved correctly"
        return 1
      fi
      ;;
    "default")
      result="$("$shell" -c ". $func_source; sc -f '$command'")"
      if [ "$result" != "default follow command updated" ]; then
        printf "follow command was not saved correctly"
        return 1
      fi
      ;;
    *)
      printf "specificity improperly configured"
      return 1
      ;;
  esac

  # Ensure that the follow command executes correctly.
  result="$("$shell" -c ". $func_source; sc integ")"
  if [ "$result" != "$expected_stdout" ]; then
    printf "follow command did not execute correctly"
    return 1
  fi

  return 0
}

test_follow_flag_shellcut_specific_simple_command() {
  _test_follow_flag "$1" "$2" "shellcut-specific" "a/b/c/d.txt" "ls" "d.txt"
}

test_follow_flag_shellcut_specific_command_with_spaces() {
  _test_follow_flag \
    "$1" \
    "$2" \
    "shellcut-specific" \
    "a/b/c/d.txt" \
    "printf success" \
    "success"
}

test_follow_flag_shellcut_specific_command_with_single_quotes() {
  _test_follow_flag \
    "$shell" \
    "$func_source" \
    "shellcut-specific" \
    "a/b/c/d.txt" \
    "printf '\\''\"success\"'\\''" \
    '"success"'
  result=$?
}

test_follow_flag_default_simple_command() {
  _test_follow_flag "$1" "$2" "default" "a/b/c/d.txt" "ls" "d.txt"
}

test_follow_flag_default_command_with_spaces() {
  _test_follow_flag \
    "$1" \
    "$2" \
    "default" \
    "a/b/c/d.txt" \
    "printf success" \
    "success"
}

test_follow_flag_default_command_with_single_quotes() {
  _test_follow_flag \
    "$shell" \
    "$func_source" \
    "default" \
    "a/b/c/d.txt" \
    "printf '\\''\"success\"'\\''" \
    '"success"'
}

script_root="$(dirname "$(readlink -fm "$0")")"
shell="$1"
func_source="$2"

# Source the utility functions.
. "$script_root/utils.sh"

# Execute all tests.
run_tests \
  "--follow" \
  "$shell" \
  "$func_source" \
  test_follow_flag_shellcut_specific_simple_command \
  test_follow_flag_shellcut_specific_command_with_spaces \
  test_follow_flag_shellcut_specific_command_with_single_quotes \
  test_follow_flag_default_simple_command \
  test_follow_flag_default_command_with_spaces \
  test_follow_flag_default_command_with_single_quotes
