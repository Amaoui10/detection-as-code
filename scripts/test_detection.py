
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS_DIR = ROOT / "tests" / "events"


def matches_rule(event):
    image = event.get("Image", "").lower()
    command_line = event.get("CommandLine", "").lower()

    is_powershell = (
        image.endswith("\\powershell.exe")
        or image.endswith("\\pwsh.exe")
    )

    has_encoded_command = "-encodedcommand" in command_line

    return is_powershell and has_encoded_command
def main():
    json_files = EVENTS_DIR.glob("**/*.json")
    total_tests = 0
    failures = 0
    for file_path in json_files:
        with file_path.open(encoding="utf-8") as file:
            data = json.load(file)

        rule_name = data["rule"]

        print(f"\nTesting rule: {rule_name}")

        for event in data["events"]:
            expected = event["expected_match"]
            actual = matches_rule(event)
            passed = expected == actual
            total_tests += 1
            if not passed:
                failures += 1
            print(
                f"{'PASS' if passed else 'FAIL'}: {event['name']} "
                f"(expected={expected}, actual={actual})"
            )
    print(f"\nResults: {total_tests - failures}/{total_tests} tests passed")

    if failures:
        raise SystemExit(1)

"""def main():
    with EVENTS_FILE.open(encoding="utf-8") as file:
        events = json.load(file)

    failures = 0

    for event in events:
        expected = event["expected_match"]
        actual = matches_rule(event)
        passed = expected == actual

        print(
            f"{'PASS' if passed else 'FAIL'}: {event['name']} "
            f"(expected={expected}, actual={actual})"
        )

        if not passed:
            failures += 1

    print(f"\nResults: {len(events) - failures}/{len(events)} tests passed")

    if failures:
        raise SystemExit(1)
"""

if __name__ == "__main__":
    main()
