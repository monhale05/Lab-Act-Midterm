"""ITECC04 Laboratory 4: checks for Part D.

Run:  python3 test_queues.py

Part D has no walkthrough. These checks are your only feedback, so read the
failures carefully. The wraparound check is the one that separates a real
circular queue from a list with a slow dequeue.
"""

from queues import CircularQueue, Deque, is_palindrome

passed = 0
failed = 0
unwritten = 0


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


def filled(capacity, items):
    q = CircularQueue(capacity)
    for item in items:
        q.enqueue(item)
    return q


print("ITECC04 Laboratory 4, Part D: CircularQueue")
print("=" * 60)

check("a new queue is empty", True, lambda: CircularQueue(3).is_empty())
check("a new queue is not full", False, lambda: CircularQueue(3).is_full())
check("a new queue has size 0", 0, lambda: CircularQueue(3).size())
check_raises("capacity 0 raises ValueError", ValueError,
             lambda: CircularQueue(0))

check("enqueue raises the size", 2, lambda: filled(3, "AB").size())
check("peek returns the first item in", "A", lambda: filled(3, "AB").peek())
check("peek leaves the size alone", 2,
      lambda: (lambda q: (q.peek(), q.size())[1])(filled(3, "AB")))


def fifo_order():
    q = filled(3, "ABC")
    return [q.dequeue(), q.dequeue(), q.dequeue()]


check("items leave in the order they arrived", ["A", "B", "C"], fifo_order)
check("filling to capacity reports full", True,
      lambda: filled(3, "ABC").is_full())
check_raises("enqueue on a full queue raises OverflowError", OverflowError,
             lambda: filled(2, "ABC"))
check_raises("dequeue on an empty queue raises IndexError", IndexError,
             lambda: CircularQueue(2).dequeue())
check_raises("peek on an empty queue raises IndexError", IndexError,
             lambda: CircularQueue(2).peek())

print()
print("wraparound: the slot freed at the front must be reused")


def wraparound_slots():
    q = filled(4, "ABC")
    q.dequeue()
    q.dequeue()
    q.enqueue("D")
    q.enqueue("E")
    return q.slots()


check("slots read ['E', None, 'C', 'D'] after wrapping",
      ["E", None, "C", "D"], wraparound_slots)


def wraparound_order():
    q = filled(4, "ABC")
    q.dequeue()
    q.dequeue()
    q.enqueue("D")
    q.enqueue("E")
    return [q.dequeue(), q.dequeue(), q.dequeue()]


check("wrapped items still leave in order", ["C", "D", "E"], wraparound_order)


def long_run():
    q = CircularQueue(3)
    seen = []
    for n in range(30):
        q.enqueue(n)
        seen.append(q.dequeue())
    return seen == list(range(30)) and q.is_empty()


check("30 enqueue and dequeue pairs on a capacity of 3", True, long_run)


def cleared_slot():
    q = filled(2, "AB")
    q.dequeue()
    return q.slots()[0]


check("a dequeued slot is cleared to None", None, cleared_slot)

print()
print("ITECC04 Laboratory 4, Part D: Deque")
print("=" * 60)

check("a new deque is empty", True, lambda: Deque().is_empty())


def both_ends():
    d = Deque()
    d.add_rear("b")
    d.add_front("a")
    d.add_rear("c")
    return [d.remove_front(), d.remove_rear(), d.remove_front()]


check("add and remove at both ends", ["a", "c", "b"], both_ends)


def deque_size():
    d = Deque()
    for item in "abcd":
        d.add_front(item)
    d.remove_rear()
    return d.size()


check("size tracks both ends", 3, deque_size)
check_raises("remove_front on empty raises IndexError", IndexError,
             lambda: Deque().remove_front())
check_raises("remove_rear on empty raises IndexError", IndexError,
             lambda: Deque().remove_rear())

print()
print("is_palindrome")
print("=" * 60)
check("'radar' is a palindrome", True, lambda: is_palindrome("radar"))
check("'Level' ignores case", True, lambda: is_palindrome("Level"))
check("'A man, a plan, a canal: Panama' ignores punctuation", True,
      lambda: is_palindrome("A man, a plan, a canal: Panama"))
check("'stack' is not a palindrome", False, lambda: is_palindrome("stack"))
check("'noon' has even length", True, lambda: is_palindrome("noon"))
check("a single letter is a palindrome", True, lambda: is_palindrome("z"))
check("an empty string is a palindrome", True, lambda: is_palindrome(""))

print()
print("=" * 60)
print(f"passed {passed}   failed {failed}   not written yet {unwritten}")
if unwritten:
    print("Write the steps named above, then run this file again.")
elif failed == 0:
    print("Part D is finished. The queue wraps, and the deque works from "
          "both ends.")
