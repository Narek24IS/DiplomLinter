#!/usr/bin/env bash

FIRST_ITEM=true

WriteSummaryHeader() {
  local SUPER_LINTER_SUMMARY_OUTPUT_PATH="${1}"

  echo "[" >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
}

WriteSummaryLineSuccess() {
  local SUPER_LINTER_SUMMARY_OUTPUT_PATH="${1}"
  local LANGUAGE_NAME="${2}"

  if [ "$FIRST_ITEM" = false ]; then
    echo ", " >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
  else
    FIRST_ITEM=false
  fi

  echo -n " {\"linter\": \"${LANGUAGE_NAME}\", \"is_success\": true}" >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
}

WriteSummaryLineFailure() {
  local SUPER_LINTER_SUMMARY_OUTPUT_PATH="${1}"
  local LANGUAGE_NAME="${2}"

  if [ "$FIRST_ITEM" = false ]; then
    echo ", " >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
  else
    FIRST_ITEM=false
  fi

  echo -n " {\"linter\": \"${LANGUAGE_NAME}\", \"is_success\": false}" >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
}

WriteSummaryFooterSuccess() {
  local SUPER_LINTER_SUMMARY_OUTPUT_PATH="${1}"
  echo "" >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
  echo -n "]" >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
}

WriteSummaryFooterFailure() {
  local SUPER_LINTER_SUMMARY_OUTPUT_PATH="${1}"
  echo "]" >>"${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
}

FormatSuperLinterSummaryFile() {
  debug "Skip file formatting cause JSON format"
}

# 0x1B (= ^[) is the control code that starts all ANSI color codes escape sequences
# Ref: https://en.wikipedia.org/wiki/ANSI_escape_code#C0_control_codes
ANSI_COLOR_CODES_SEARCH_PATTERN='\x1b\[[0-9;]*m'
export ANSI_COLOR_CODES_SEARCH_PATTERN
RemoveAnsiColorCodesFromFile() {
  local FILE_PATH="${1}"
  debug "Removing ANSI color codes from ${FILE_PATH}"
  if ! sed -i "s/${ANSI_COLOR_CODES_SEARCH_PATTERN}//g" "${FILE_PATH}"; then
    debug "[error] Error while removing ANSI color codes from ${FILE_PATH}"
    return 1
  fi
}
