"""ITECC04 Laboratory 4: checks for Parts B and C.

Run:  python3 test_expression.py

The twelve conversion cases come from ITECC04_Ch4_expression_cases.csv, the
same file posted on the LMS. Open it: the last column says what each case is
testing, so a failing case tells you which rule you have not implemented.

If the CSV is missing, the file falls back to the same cases written inline,
so the checks still run.
"""

import csv
import os

from expression import infix_to_postfix, evaluate_postfix, apply_operator

CASES_FILE = "ITECC04_Ch4_expression_cases.csv"

FALLBACK = [
    ("3 + 4 * 2", "3 4 2 * +", 11),
    ("( 3 + 4 ) * 2", "3 4 + 2 *", 14),
    ("3 + 4 * 2 / ( 1 - 5 )", "3 4 2 * 1 5 - / +", 1),
    ("10 - 2 - 3", "10 2 - 3 -", 5),
    ("8 / 4 / 2", "8 4 / 2 /", 1),
    ("2 ^ 3 ^ 2", "2 3 2 ^ ^", 512),
    ("( 2 ^ 3 ) ^ 2", "2 3 ^ 2 ^", 64),
    ("( 1 + 2 ) * ( 3 + 4 )", "1 2 + 3 4 + *", 21),
    ("5 + 6 % 4", "5 6 4 % +", 7),
    ("( ( 2 + 3 ) * 4 - 6 ) / 7", "2 3 + 4 * 6 - 7 /", 2),
    ("42", "42", 42),
    ("7 * 6", "7 6 *", 42),
]

passed = 0
failed = 0
unwritten = 0


def load_cases():
    if not os.path.exists(CASES_FILE):
        print(f"  note: {CASES_FILE} not found, using the built-in cases")
        return FALLBACK
    rows = []
    with open(CASES_FILE, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append((row["infix"], row["expected_postfix"],
                         float(row["expected_value"])))
    return rows


def check(label, expected, produce):
    global passed, failed, unwritten
    try:
        actual = produce()
    except NotImplementedError as unfinished:
        unwritten += 1
        print(f"  [ ] {label}  <- not written yet: {unfinished}")
        return
    except Exception as error:
        failed += 1
        print(f"  [X] {label}  <- {type(error).__name__}: {error}")
        return
    if actual == expected:
        passed += 1
        print(f"  [OK] {label}")
    else:
        failed += 1
        print(f"  [X] {label}  <- expected {expected!r}, got {actual!r}")


def check_raises(label, error_type, produce):
    global passed, failed, unwritten
    try:
        produce()
    except NotImplementedError as unfinished:
        unwritten += 1
        print(f"  [ ] {label}  <- not written yet: {unfinished}")
        return
    except error_type:
        passed += 1
        print(f"  [OK] {label}")
        return
    except Exception as error:
        failed += 1
        print(f"  [X] {label}  <- raised {type(error).__name__}, wanted "
              f"{error_type.__name__}")
        return
    failed += 1
    print(f"  [X] {label}  <- nothing was raised, wanted {error_type.__name__}")


cases = load_cases()

print("ITECC04 Laboratory 4, Part B: infix to postfix")
print("=" * 60)
for infix, postfix, _ in cases:
    check(f"{infix}  ->  {postfix}", postfix,
          lambda i=infix: infix_to_postfix(i))

print()
print("unbalanced parentheses must be refused")
check_raises("( 1 + 2   raises ValueError", ValueError,
             lambda: infix_to_postfix("( 1 + 2"))
check_raises("1 + 2 )   raises ValueError", ValueError,
             lambda: infix_to_postfix("1 + 2 )"))

print()
print("ITECC04 Laboratory 4, Part C: postfix evaluation")
print("=" * 60)
for _, postfix, value in cases:
    check(f"{postfix}  =  {value:g}", value,
          lambda p=postfix: evaluate_postfix(p))

print()
print("operand order must be correct")
check("5 3 -  is 2 and not -2", 2.0, lambda: evaluate_postfix("5 3 -"))
check("8 2 /  is 4 and not 0.25", 4.0, lambda: evaluate_postfix("8 2 /"))
check("2 3 ^  is 8 and not 9", 8.0, lambda: evaluate_postfix("2 3 ^"))

print()
print("malformed input must be refused")
check_raises("3 +      raises ValueError", ValueError,
             lambda: evaluate_postfix("3 +"))
check_raises("1 2 3 +  raises ValueError", ValueError,
             lambda: evaluate_postfix("1 2 3 +"))
check_raises("4 0 /    raises ZeroDivisionError", ZeroDivisionError,
             lambda: evaluate_postfix("4 0 /"))
check_raises("apply_operator with '$' raises ValueError", ValueError,
             lambda: apply_operator("$", 1.0, 2.0))

print()
print("=" * 60)
print(f"passed {passed}   failed {failed}   not written yet {unwritten}")
if unwritten:
    print("Write the steps named above, then run this file again.")
elif failed == 0:
    print("Parts B and C are finished. Every case in the CSV converts and "
          "evaluates correctly.")
