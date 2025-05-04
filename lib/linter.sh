#!/usr/bin/env bash

set -o nounset
set -o pipefail

###########
# GLOBALS #
###########
DEFAULT_RULES_LOCATION='/action/lib/.automation'                            # Default rules files location
DEFAULT_SUPER_LINTER_WORKSPACE="/tmp/lint"                                  # Fall-back value for the workspace
DEFAULT_WORKSPACE="${DEFAULT_WORKSPACE:-${DEFAULT_SUPER_LINTER_WORKSPACE}}" # Default workspace if running locally
# shellcheck disable=SC2034
GITHUB_WORKSPACE=${DEFAULT_WORKSPACE}
TEST_CASE_RUN="false"
FILTER_REGEX_INCLUDE="${FILTER_REGEX_INCLUDE:-""}"
export FILTER_REGEX_INCLUDE
FILTER_REGEX_EXCLUDE="${FILTER_REGEX_EXCLUDE:-""}"
export FILTER_REGEX_EXCLUDE
# shellcheck disable=SC2034 # Variable is referenced in other scripts
RAW_FILE_ARRAY=() # Array of all files that were changed

#########################
# Source Function Files #
#########################
# Source log functions and variables early so we can use them ASAP
# shellcheck source=/dev/null
source /action/lib/functions/log.sh # Source the function script(s)

# shellcheck source=/dev/null
source /action/lib/functions/buildFileList.sh # Source the function script(s)
# shellcheck source=/dev/null
source /action/lib/functions/detectFiles.sh # Source the function script(s)
# shellcheck source=/dev/null
source /action/lib/functions/linterRules.sh # Source the function script(s)
# shellcheck source=/dev/null
source /action/lib/functions/validation.sh # Source the function script(s)
# shellcheck source=/dev/null
source /action/lib/functions/worker.sh # Source the function script(s)
# shellcheck source=/dev/null
source /action/lib/functions/output.sh

declare -l BASH_EXEC_IGNORE_LIBRARIES
BASH_EXEC_IGNORE_LIBRARIES="${BASH_EXEC_IGNORE_LIBRARIES:-false}"

declare -l DISABLE_ERRORS
DISABLE_ERRORS="${DISABLE_ERRORS:-"false"}"

declare -l IGNORE_GENERATED_FILES
# Do not ignore generated files by default for backwards compatibility
IGNORE_GENERATED_FILES="${IGNORE_GENERATED_FILES:-false}"
export IGNORE_GENERATED_FILES

declare -l IGNORE_GITIGNORED_FILES
IGNORE_GITIGNORED_FILES="${IGNORE_GITIGNORED_FILES:-false}"
export IGNORE_GITIGNORED_FILES

declare -l SAVE_SUPER_LINTER_OUTPUT
SAVE_SUPER_LINTER_OUTPUT="${SAVE_SUPER_LINTER_OUTPUT:-false}"

declare -l SUPPRESS_FILE_TYPE_WARN
SUPPRESS_FILE_TYPE_WARN="${SUPPRESS_FILE_TYPE_WARN:-false}"

declare -l USE_FIND_ALGORITHM
USE_FIND_ALGORITHM="${USE_FIND_ALGORITHM:-false}"

declare -l VALIDATE_ALL_CODEBASE
VALIDATE_ALL_CODEBASE="${VALIDATE_ALL_CODEBASE:-"true"}"

declare -l YAML_ERROR_ON_WARNING
YAML_ERROR_ON_WARNING="${YAML_ERROR_ON_WARNING:-false}"

declare -l SAVE_SUPER_LINTER_SUMMARY
SAVE_SUPER_LINTER_SUMMARY="${SAVE_SUPER_LINTER_SUMMARY:-false}"

declare -l REMOVE_ANSI_COLOR_CODES_FROM_OUTPUT
REMOVE_ANSI_COLOR_CODES_FROM_OUTPUT="${REMOVE_ANSI_COLOR_CODES_FROM_OUTPUT:-"false"}"
export REMOVE_ANSI_COLOR_CODES_FROM_OUTPUT

declare GROOVY_FAILON_LEVEL
GROOVY_FAILON_LEVEL="${GROOVY_FAILON_LEVEL:-"warning"}"
export GROOVY_FAILON_LEVEL

# Define private output paths early because cleanup depends on those being defined
DEFAULT_SUPER_LINTER_OUTPUT_DIRECTORY_NAME="super-linter-output"
SUPER_LINTER_OUTPUT_DIRECTORY_NAME="${SUPER_LINTER_OUTPUT_DIRECTORY_NAME:-${DEFAULT_SUPER_LINTER_OUTPUT_DIRECTORY_NAME}}"
export SUPER_LINTER_OUTPUT_DIRECTORY_NAME
debug "Super-linter main output directory name: ${SUPER_LINTER_OUTPUT_DIRECTORY_NAME}"

SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH="/tmp/${DEFAULT_SUPER_LINTER_OUTPUT_DIRECTORY_NAME}"
export SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH
debug "Super-linter private output directory path: ${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH}"
mkdir -p "${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH}"

FIX_MODE_ENABLED="false"

ValidateBooleanConfigurationVariables

# Set the log level
TF_LOG_LEVEL="info"
if [[ "${LOG_DEBUG}" == "true" ]]; then
  TF_LOG_LEVEL="debug "
fi
export TF_LOG_LEVEL
debug "TF_LOG_LEVEL: ${TF_LOG_LEVEL}"
TFLINT_LOG="${TF_LOG_LEVEL}"
export TFLINT_LOG
debug "TFLINT_LOG: ${TFLINT_LOG}"

# Load linter configuration and rules files
# shellcheck source=/dev/null
source /action/lib/globals/linterRules.sh

# Load languages array
# shellcheck source=/dev/null
source /action/lib/globals/languages.sh


# shellcheck disable=SC2317
cleanup() {
  local -ri EXIT_CODE=$?
  debug "Captured exit code: ${EXIT_CODE}"

  if [ -n "${DEFAULT_WORKSPACE:-}" ]; then
    debug "Removing temporary files and directories"
    rm -rf \
      "${DEFAULT_WORKSPACE}/.mypy_cache" \
      "${DEFAULT_WORKSPACE}/logback.log" \
      "${DEFAULT_WORKSPACE}/.ruff_cache"

    if [[ "${SUPER_LINTER_COPIED_R_LINTER_RULES_FILE:-}" == "true" ]]; then
      debug "Deleting ${R_RULES_FILE_PATH_IN_ROOT} because super-linter created it."
      rm -rf "${R_RULES_FILE_PATH_IN_ROOT}"
    fi

    # Define this variable here so we can rely on it as soon as possible
    local LOG_FILE_PATH="${DEFAULT_WORKSPACE}/${LOG_FILE}"
    debug "LOG_FILE_PATH: ${LOG_FILE_PATH}"
    if [ "${CREATE_LOG_FILE}" = "true" ]; then
      if [[ "${REMOVE_ANSI_COLOR_CODES_FROM_OUTPUT}" == "true" ]] &&
        ! RemoveAnsiColorCodesFromFile "${LOG_TEMP}"; then
        fatal "Error while removing ANSI color codes from ${LOG_TEMP}"
      fi
      debug "Moving log file from ${LOG_TEMP} to ${LOG_FILE_PATH}"
      mv \
        --force \
        "${LOG_TEMP}" "${LOG_FILE_PATH}"
    else
      debug "Skip moving the log file from ${LOG_TEMP} to ${LOG_FILE_PATH}"
    fi

    if [ "${SAVE_SUPER_LINTER_OUTPUT}" = "true" ]; then
      debug "Super-linter output directory path is set to ${SUPER_LINTER_OUTPUT_DIRECTORY_PATH:-"not set"}"
      if [[ -n "${SUPER_LINTER_OUTPUT_DIRECTORY_PATH:-}" ]]; then
        debug "Super-linter output directory path is set to ${SUPER_LINTER_OUTPUT_DIRECTORY_PATH}"
        if [ -e "${SUPER_LINTER_OUTPUT_DIRECTORY_PATH}" ]; then
          debug "${SUPER_LINTER_OUTPUT_DIRECTORY_PATH} already exists. Deleting it before moving the new output directory there."
          rm -fr "${SUPER_LINTER_OUTPUT_DIRECTORY_PATH}"
        fi
        debug "Moving Super-linter output from ${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH} to ${SUPER_LINTER_OUTPUT_DIRECTORY_PATH}"
        mv "${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH}" "${SUPER_LINTER_OUTPUT_DIRECTORY_PATH}"
      else
        debug "Skip moving the private Super-linter output directory (${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH}) to the output directory because the Super-linter output destination directory path is not initialized yet"
      fi
    else
      debug "Skip moving the private Super-linter output directory (${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH}) to the output directory (${SUPER_LINTER_OUTPUT_DIRECTORY_PATH:-"not initialized yet"})"
    fi

  else
    debug "DEFAULT_WORKSPACE is not set. Skipping filesystem cleanup steps"
  fi

  exit "${EXIT_CODE}"
  trap - 0 1 2 3 6 14 15
}
trap 'cleanup' 0 1 2 3 6 14 15

# Print linter versions
debug "This version of Super-linter includes the following tools:\n$(cat "${VERSION_FILE}")"

TYPESCRIPT_STANDARD_TSCONFIG_FILE="${DEFAULT_WORKSPACE}/${TYPESCRIPT_STANDARD_TSCONFIG_FILE:-"tsconfig.json"}"
debug "TYPESCRIPT_STANDARD_TSCONFIG_FILE: ${TYPESCRIPT_STANDARD_TSCONFIG_FILE}"

R_RULES_FILE_PATH_IN_ROOT="${DEFAULT_WORKSPACE}/${R_FILE_NAME}"
debug "R_RULES_FILE_PATH_IN_ROOT: ${R_RULES_FILE_PATH_IN_ROOT}"

SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH="${DEFAULT_WORKSPACE}/${SUPER_LINTER_OUTPUT_DIRECTORY_NAME}"
export SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH
debug "Super-linter main output directory path: ${SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH}"

SUPER_LINTER_OUTPUT_DIRECTORY_PATH="${SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH}/super-linter"
export SUPER_LINTER_OUTPUT_DIRECTORY_PATH
debug "Super-linter output directory path: ${SUPER_LINTER_OUTPUT_DIRECTORY_PATH}"

SUPER_LINTER_SUMMARY_OUTPUT_PATH="${SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH}/${SUPER_LINTER_SUMMARY_FILE_NAME:-"super-linter-summary.md"}"
export SUPER_LINTER_SUMMARY_OUTPUT_PATH
debug "Super-linter summary output path: ${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"

# Ensure that the main output directory and files exist because the user might not have created them
# before running Super-linter. These conditions list all the cases that require an output
# directory to be there.
if [[ "${SAVE_SUPER_LINTER_OUTPUT}" = "true" ]] ||
  [[ "${SAVE_SUPER_LINTER_SUMMARY}" == "true" ]] ||
  [[ "${CREATE_LOG_FILE}" = "true" ]]; then
  debug "Ensure that ${SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH} exists"
  mkdir -p "${SUPER_LINTER_MAIN_OUTPUT_DIRECTORY_PATH}"
fi

if [[ "${SAVE_SUPER_LINTER_SUMMARY}" == "true" ]]; then
  debug "Remove eventual ${SUPER_LINTER_SUMMARY_OUTPUT_PATH} leftover"
  rm -f "${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"

  debug "Ensuring that ${SUPER_LINTER_SUMMARY_OUTPUT_PATH} exists."
  if ! touch "${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"; then
    fatal "Cannot create Super-linter summary file: ${SUPER_LINTER_SUMMARY_OUTPUT_PATH}"
  fi
fi

############################
# Validate the environment #
############################
debug "--------------------------------------------"
debug "Validating the configuration"
if ! ValidateFindMode; then
  fatal "Error while validating the configuration."
fi
if ! ValidateValidationVariables; then
  fatal "Error while validating the configuration of enabled linters"
fi
if ! ValidateAnsibleDirectory; then
  fatal "Error while validating the configuration of the Ansible directory"
fi

ValidateDeprecatedVariables

# After checking if LOG_LEVEL is set to a deprecated value (see the ValidateDeprecatedVariables function),
# we can unset it so other programs that rely on this variable, such as Checkov and renovate-config-validator
# don't get confused.
unset LOG_LEVEL

#################################
# Get the linter rules location #
#################################
LinterRulesLocation

########################
# Get the linter rules #
########################
for LANGUAGE in "${LANGUAGE_ARRAY_FOR_LINTER_RULES[@]}"; do
  debug "Loading rules for ${LANGUAGE}..."
  eval "GetLinterRules ${LANGUAGE} ${DEFAULT_RULES_LOCATION}"
done

# Load rules for special cases
GetStandardRules "javascript"

#############################################################################
# Validate the environment that depends on linter rules variables being set #
#############################################################################

# We need the variables defined in linterCommandsOptions to initialize FIX_....
# variables.
# shellcheck source=/dev/null
source /action/lib/globals/linterCommandsOptions.sh
if ! ValidateCheckModeAndFixModeVariables; then
  fatal "Error while validating the configuration fix mode for linters that support that"
fi

###########################################
# Build the list of files for each linter #
###########################################
BuildFileList "${VALIDATE_ALL_CODEBASE}" "${TEST_CASE_RUN}"

#####################################
# Run additional Installs as needed #
#####################################
RunAdditionalInstalls

###############
# Run linters #
###############
declare PARALLEL_RESULTS_FILE_PATH
PARALLEL_RESULTS_FILE_PATH="${SUPER_LINTER_PRIVATE_OUTPUT_DIRECTORY_PATH}/super-linter-results.json"
debug "PARALLEL_RESULTS_FILE_PATH: ${PARALLEL_RESULTS_FILE_PATH}"

declare -i LINTING_MAX_PROCS
LINTING_MAX_PROCS=$(nproc)

CheckIfFixModeIsEnabled
if [[ "${FIX_MODE_ENABLED}" == "true" ]]; then
  # This slows down the fix process, but avoids that linters that work on the same
  # types of files try opening the same file at the same time
  LINTING_MAX_PROCS=1
  debug "Set LINTING_MAX_PROCS to ${LINTING_MAX_PROCS} to avoid that linters and formatters edit the same file at the same time."
fi

declare -a PARALLEL_COMMAND
PARALLEL_COMMAND=(parallel --will-cite --keep-order --max-procs "$((LINTING_MAX_PROCS))" --xargs --results "${PARALLEL_RESULTS_FILE_PATH}")

# Run one LANGUAGE per process. Each of these processes will run more processees in parellel if supported
PARALLEL_COMMAND+=(--max-lines 1)

if [ "${LOG_DEBUG}" == "true" ]; then
  debug "LOG_DEBUG is enabled. Enable verbose ouput for parallel"
  PARALLEL_COMMAND+=(--verbose)
fi

PARALLEL_COMMAND+=("LintCodebase" "{}" "\"${TEST_CASE_RUN}\"")
debug "PARALLEL_COMMAND: ${PARALLEL_COMMAND[*]}"

PARALLEL_COMMAND_OUTPUT=$(printf "%s\n" "${LANGUAGE_ARRAY[@]}" | "${PARALLEL_COMMAND[@]}" 2>&1)
PARALLEL_COMMAND_RETURN_CODE=$?
debug "PARALLEL_COMMAND_OUTPUT when running linters (exit code: ${PARALLEL_COMMAND_RETURN_CODE}):\n${PARALLEL_COMMAND_OUTPUT}"
debug "Parallel output file (${PARALLEL_RESULTS_FILE_PATH}) contents when running linters:\n$(cat "${PARALLEL_RESULTS_FILE_PATH}")"

RESULTS_OBJECT=
if ! RESULTS_OBJECT=$(jq --raw-output -n '[inputs]' "${PARALLEL_RESULTS_FILE_PATH}"); then
  fatal "Error loading results when building the file list: ${RESULTS_OBJECT}"
fi
info "RESULTS_OBJECT when running linters:\n${RESULTS_OBJECT}"

# Get raw output so we can strip quotes from the data we load. Also, strip the final newline to avoid adding it two times
if ! STDOUT_LINTERS="$(jq --raw-output '.[] | select(.Stdout[:-1] | length > 0) | .Stdout[:-1]' <<<"${RESULTS_OBJECT}")"; then
  fatal "Error when loading stdout when running linters:\n${STDOUT_LINTERS}"
fi

if [ -n "${STDOUT_LINTERS}" ]; then
  info "Command output when running linters:\n------\n${STDOUT_LINTERS}\n------"
else
  debug "Stdout when running linters is empty"
fi

if ! STDERR_LINTERS="$(jq --raw-output '.[] | select(.Stderr[:-1] | length > 0) | .Stderr[:-1]' <<<"${RESULTS_OBJECT}")"; then
  fatal "Error when loading stderr for ${FILE_TYPE}:\n${STDERR_LINTERS}"
fi

if [ -n "${STDERR_LINTERS}" ]; then
  info "Stderr when running linters:\n------\n${STDERR_LINTERS}\n------"
else
  debug "Stderr when running linters is empty"
fi

if [[ ${PARALLEL_COMMAND_RETURN_CODE} -ne 0 ]]; then
  fatal "Error when running linters. Exit code: ${PARALLEL_COMMAND_RETURN_CODE}"
fi
