![Sigma Rules Validation](https://github.com/amaoui10/detection-as-code/actions/workflows/sigma-validation.yml/badge.svg)

# Detection as Code

An automated Detection as Code pipeline for validating, testing, and backtesting Windows security detection rules using Sigma, RSigma, and GitHub Actions.

## Overview

This project demonstrates how security detection rules can be managed as code and tested automatically before deployment.

It uses Sigma rules to identify suspicious Windows activity, simulated security events to validate detection logic, and RSigma to evaluate detection results against predefined expectations.

GitHub Actions automates the validation and backtesting process whenever changes are pushed or a pull request is opened against the `main` branch.

## Project Objectives

- Develop structured detection rules using the Sigma format.
- Validate Sigma rule syntax automatically.
- Test detection logic against simulated Windows security events.
- Verify expected detection counts and prevent unexpected detections.
- Automate the testing process through a CI/CD workflow.

## Architecture

```text
detection-as-code/
│
├── .github/
│   └── workflows/
│       └── sigma-validation.yml
│
├── rules/
│   └── windows/
│       ├── win_powershell_encoded_command.yml
│       └── win_user_account_created.yml
│
├── tests/
│   ├── events/
│   │   └── windows/
│   │       ├── powershell.ndjson
│   │       └── user_account.ndjson
│   │
│   └── expectations.yml
│
└── README.md
```

### Main Components

| Component | Responsibility |
|---|---|
| `rules/` | Contains Sigma detection rules. |
| `tests/events/` | Contains simulated Windows security events in NDJSON format. |
| `tests/expectations.yml` | Defines the expected number of detections for each rule. |
| `sigma-cli` | Validates Sigma rule syntax. |
| `RSigma` | Executes detection rules against test events and performs backtesting. |
| `GitHub Actions` | Automates validation and backtesting. |

## Detection Rules

### 1. PowerShell Encoded Command Execution

**File:** `win_powershell_encoded_command.yml`

Detects PowerShell execution involving the `-EncodedCommand` parameter.

This behavior can be associated with attempts to hide commands through Base64 encoding.

### 2. Local User Account Creation

**File:** `win_user_account_created.yml`

Detects Windows Security Event ID `4720`, generated when a local user account is created.

Unexpected account creation can indicate suspicious activity or potential persistence.

## Testing Strategy

Each detection rule is tested against simulated events.

The test datasets include:

- **Positive events:** Events expected to trigger a detection rule.
- **Negative events:** Events that should not trigger the rule.

Events are stored in NDJSON format, with one JSON event per line.

The `expectations.yml` file defines the expected number of detections for each rule.

RSigma evaluates the rules against the test corpus and checks whether the results match the defined expectations.

Unexpected detections are configured to fail the backtest.

## CI/CD Pipeline

GitHub Actions automatically runs the following steps:

1. Checks out the repository.
2. Installs Sigma CLI.
3. Validates all Sigma rules.
4. Installs RSigma.
5. Runs the RSigma backtest against the test corpus.
6. Fails the workflow if validation or backtesting fails.

The workflow is triggered by:

- Pushes to the `main` branch.
- Pull requests targeting the `main` branch.

## Running Locally

### Requirements

- Python and pip (required to install Sigma CLI).
- Sigma CLI.
- RSigma.

### 1. Validate Sigma Rules

```bash
sigma check rules/windows/*.yml
```

### 2. Run the Backtest

```bash
rsigma rule backtest \
  -r rules/windows/ \
  --corpus tests/events/windows/ \
  --expectations tests/expectations.yml \
  --unexpected fail
```

The backtest checks whether the detection rules produce the expected results against the simulated events.

## Current Test Results

Latest successful local backtest:

| Metric | Result |
|---|---:|
| Corpus files | 2 |
| Events processed | 5 |
| Expectations passed | 2/2 |
| Unexpected detections | 0 |

The GitHub Actions workflow also completed successfully after the integration of both detection rules.

## Project Scope

This project focuses on the development, validation, and automated testing of Sigma detection rules.

It does not currently implement real-time log monitoring, centralized log collection, or SIEM functionality.

The test events are simulated and are intended to validate detection logic rather than represent a production Windows environment.

## Technologies

- Sigma
- Sigma CLI
- RSigma
- Python (installation dependency for Sigma CLI)
- YAML
- JSON / NDJSON
- GitHub Actions

