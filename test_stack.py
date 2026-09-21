"""ITECC04 Laboratory 4: checks for Part A.

Run:  python3 test_stack.py

The SAME fourteen checks run against both stacks. That is the point of the
part: two different storage strategies, one contract. If a check passes for
one class and fails for the other, the two are not interchangeable yet.
"""

from stack_array import ArrayStack
from stack_linked import LinkedStack

passed = 0
failed = 0
unwritten = 0


def check(label, expected, produce):
    """Runs one check and prints one line."""
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
    """Passes only when the named error is raised."""
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


def run_suite(name, Stack):
    print(f"\n{name}")

    check("a new stack is empty", True, lambda: Stack().is_empty())
    check("a new stack has size 0", 0, lambda: Stack().size())

    def push_one():
        s = Stack()
        s.push("a")
        return s.size()
    check("push makes the size 1", 1, push_one)

    def push_three_peek():
        s = Stack()
        for item in ["a", "b", "c"]:
            s.push(item)
        return s.peek()
    check("peek returns the last item pushed", "c", push_three_peek)

    def peek_does_not_remove():
        s = Stack()
        s.push("a")
        s.peek()
        s.peek()
        return s.size()
    check("peek leaves the size alone", 1, peek_does_not_remove)

    def pop_order():
        s = Stack()
        for item in [1, 2, 3]:
            s.push(item)
        return [s.pop(), s.pop(), s.pop()]
    check("items come off in reverse order", [3, 2, 1], pop_order)

    def pop_reduces_size():
        s = Stack()
        s.push("a")
        s.push("b")
        s.pop()
        return s.size()
    check("pop reduces the size", 1, pop_reduces_size)

    def empty_after_popping_all():
        s = Stack()
        s.push("a")
        s.pop()
        return s.is_empty()
    check("popping everything empties the stack", True, empty_after_popping_all)

    check_raises("pop on empty raises IndexError", IndexError,
                 lambda: Stack().pop())
    check_raises("peek on empty raises IndexError", IndexError,
                 lambda: Stack().peek())

    def reuse_after_empty():
        s = Stack()
        s.push("a")
        s.pop()
        s.push("b")
        return s.peek()
    check("the stack works again after emptying", "b", reuse_after_empty)

    def holds_any_type():
        s = Stack()
        s.push(1)
        s.push("two")
        s.push([3])
        return s.pop()
    check("any type may be stored", [3], holds_any_type)

    def len_works():
        s = Stack()
        s.push("a")
        s.push("b")
        return len(s)
    check("len(stack) matches size()", 2, len_works)

    def deep_stack():
        s = Stack()
        for n in range(500):
            s.push(n)
        for _ in range(499):
            s.pop()
        return s.pop()
    check("500 pushes and 500 pops end at the first item", 0, deep_stack)


print("ITECC04 Laboratory 4, Part A")
print("=" * 60)
run_suite("ArrayStack  (stack_array.py)", ArrayStack)
run_suite("LinkedStack (stack_linked.py)", LinkedStack)

print()
print("=" * 60)
print(f"passed {passed}   failed {failed}   not written yet {unwritten}")
if unwritten:
    print("Write the steps named above, then run this file again.")
elif failed == 0:
    print("Part A is finished. Both stacks satisfy the same contract.")