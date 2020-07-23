#!/bin/sh

test_delete_flag_existent_shellcut() {
  shell="$1"
  func_source="$2"

  # Remove the custom Shellcuts configuration file if it exists.
  rm -f "$SHELLCUTS_CONF"

  # Create a shellcut.
  first_result="$("$shell" -c ". $func_source; sc -n integ-test")"
  if [ "$first_result" != 'new shellcut "integ-test" created' ]; then
    printf "shellcut could not be created"
    return 1
  fi

  # Ensure that the shellcut is added to the configuration file.
  grep -q "integ-test" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "shellcut could not be found in the configuration file"
    return 1
  fi

  # Delete the shellcut.
  second_result="$("$shell" -c ". $func_source; sc -d integ-test")"
  if [ "$second_result" != 'shellcut "integ-test" deleted' ]; then
    printf "shellcut could not be deleted"
    return 1
  fi

  grep -q "integ-test" "$SHELLCUTS_CONF"
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
  first_result="$("$shell" -c ". $func_source; sc -n integ-test-preserved")"
  if [ "$first_result" != 'new shellcut "integ-test-preserved" created' ]; then
    printf "preserved shellcut could not be created"
    return 1
  fi

  # Ensure that the preserved shellcut is added to the configuration file.
  grep -q "integ-test-preserved" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "preserved shellcut could not be found in the configuration file"
    return 1
  fi

  # Delete a different, nonexistent shellcut.
  second_result="$("$shell" -c ". $func_source; sc -d integ-test-nonexistent")"
  if [ "$second_result" != 'shellcut "integ-test-nonexistent" deleted' ]; then
    printf "nonexistent shellcut could not be deleted"
    return 1
  fi

  # Ensure that the preserved shellcut still exists.
  grep -q "integ-test-preserved" "$SHELLCUTS_CONF"
  if [ $? -ne 0 ]; then
    printf "preserved shellcut could not be found in the configuration file"
    return 1
  fi

  # Ensure that the nonexistent shellcut is still not in the configuration file.
  grep -q "integ-test-nonexistent" "$SHELLCUTS_CONF"
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
