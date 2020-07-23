#!/bin/sh

# Format and print a failure message.
_fail() {
  failed=$((failed + 1))
  printf "  \e[1;31mFAILED: $1 ($2)\e[0m\n"
}

# Format and print a pass message.
_pass() {
  printf "  \e[1;32mPASSED: $1\e[0m\n"
}

# Verify that certain expected environmental conditions are met for the tests.
_verify_environment() {
  if [ "$#" -lt 4 ]; then
    printf "Must provide a type, shell, function source file, and list of tests.\n"

    return 1
  fi

  shell="$2"
  func_source="$3"

  case "$shell" in
    bash | dash | ksh | fish | zsh)
      :
      ;;
    *)
      printf "First argument is not a supported shell.\n"

      return 1
      ;;
  esac

  if [ ! -f "$func_source" ]; then
    printf "Second argument is a non-existent path.\n"

    return 1
  fi

  return 0
}

# To prevent erasure of developers' personal configuration files the tests use
# a custom configuration file.
export SHELLCUTS_CONF="/tmp/shellcuts-integ-test-conf"

# Run all provided tests.
run_tests() {
  _verify_environment "$@"
  if [ $? -ne 0 ]; then
    return 1
  fi

  type="$1"
  shell="$2"
  func_source="$3"
  shift
  shift
  shift

  failed=0

  printf "Running $type tests using $shell shell...\n"
  for test_name in "$@"; do
    error="$($test_name "$shell" "$func_source")"
    [ $? -ne 0 ] && _fail "$test_name" "$error" || _pass "$test_name"
  done

  return $failed
}
