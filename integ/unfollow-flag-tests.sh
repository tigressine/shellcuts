#!/bin/sh

test_unfollow_flag_specific_shellcut_follow() {
  shell="$1"
  func_source="$2"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Create a shellcut with a follow command.
  result="$("$shell" -c ". $func_source; sc -n integ follow")"
  if [ "$result" != 'new shellcut "integ" created' ]; then
    printf "shellcut could not be created"
    return 1
  fi

  # Ensure that the shellcut's follow command is added to the configuration
  # file.
  grep -q "follow" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "follow command could not be found in the configuration file"
    return 1
  fi

  # Delete the shellcut's follow command.
  result="$("$shell" -c ". $func_source; sc -u integ")"
  if [ "$result" != 'follow command removed for shellcut "integ"' ]; then
    printf "follow command could not be deleted"
    return 1
  fi

  # Ensure that the follow command has been removed from the configuration file.
  grep -q "follow" "$SHELLCUTS_CONF"
  if [ $? -eq 0 ]; then
    printf "follow command was still found in the configuration file"
    return 1
  fi

  return 0
}

test_unfollow_flag_default_follow() {
  shell="$1"
  func_source="$2"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Create a default follow command.
  result="$("$shell" -c ". $func_source; sc -f follow")"
  if [ "$result" != "default follow command updated" ]; then
    printf "default follow command could not be created"
    return 1
  fi

  # Ensure that the default follow command is added to the configuration file.
  grep -q "follow" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "default follow command could not be found in the configuration file"
    return 1
  fi

  # Delete the default follow command.
  result="$("$shell" -c ". $func_source; sc -u")"
  if [ "$result" != "default follow command removed" ]; then
    printf "default follow command could not be deleted"
    return 1
  fi

  # Ensure that the follow command has been removed from the configuration file.
  grep -q "follow" "$SHELLCUTS_CONF"
  if [ $? -eq 0 ]; then
    printf "default follow command was still found in the configuration file"
    return 1
  fi

  return 0
}

script_root="$(dirname "$(readlink -fm "$0")")"
shell="$1"
func_source="$2"

# Source the utility functions.
. "$script_root/utils.sh"

# Execute all tests.
run_tests \
  "--unfollow" \
  "$shell" \
  "$func_source" \
  test_unfollow_flag_specific_shellcut_follow \
  test_unfollow_flag_default_follow
