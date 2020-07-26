#!/bin/sh

test_delete_flag_existent_shellcut() {
  shell="$1"
  func_source="$2"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Create a shellcut.
  result="$("$shell" -c ". $func_source; sc -n integ")"
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

  # Delete the shellcut.
  result="$("$shell" -c ". $func_source; sc -d integ")"
  if [ "$result" != 'shellcut "integ" deleted' ]; then
    printf "shellcut could not be deleted"
    return 1
  fi

  grep -q "integ" "$SHELLCUTS_CONF"
  if [ $? -eq 0 ]; then
    printf "shellcut was still found in the configuration file"
    return 1
  fi

  return 0
}

test_delete_flag_nonexistent_shellcut() {
  shell="$1"
  func_source="$2"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Create a shellcut that should be preserved.
  result="$("$shell" -c ". $func_source; sc -n integ-preserved")"
  if [ "$result" != 'new shellcut "integ-preserved" created' ]; then
    printf "preserved shellcut could not be created"
    return 1
  fi

  # Ensure that the preserved shellcut is added to the configuration file.
  grep -q "integ-preserved" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "preserved shellcut could not be found in the configuration file"
    return 1
  fi

  # Delete a different, nonexistent shellcut.
  result="$("$shell" -c ". $func_source; sc -d integ-nonexistent")"
  if [ "$result" != 'shellcut "integ-nonexistent" deleted' ]; then
    printf "nonexistent shellcut could not be deleted"
    return 1
  fi

  # Ensure that the preserved shellcut still exists.
  grep -q "integ-preserved" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "preserved shellcut could not be found in the configuration file"
    return 1
  fi

  # Ensure that the nonexistent shellcut is still not in the configuration file.
  grep -q "integ-nonexistent" "$SHELLCUTS_CONF"
  if [ $? -eq 0 ]; then
    printf "shellcut found in the configuration file shouldn't exist"
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
  "--delete" \
  "$shell" \
  "$func_source" \
  test_delete_flag_existent_shellcut \
  test_delete_flag_nonexistent_shellcut
