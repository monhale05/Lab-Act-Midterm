"""ITECC04 Laboratory 4, Part A1: the array-based stack.

Fill in one step at a time. Run test_stack.py after every step.

The list is the storage, and the END of the list is the top. That single
decision is what makes push and pop cost O(1): appending and popping at the
end of a Python list does not move any other element. Choosing index 0 as the
top would make every operation shift the whole list.

Nothing outside this class may touch self._items. That is the encapsulation
the rubric marks.
"""


class ArrayStack:

    def __init__(self):
        """Step 1. Create the empty list that will hold the items."""
        self._items = []

    def push(self, item):
        """Step 2. Put an item on top. No return value.

        One line. Use the list method that adds at the end.
        """
        self._items.append(item)

    def pop(self):
        """Step 3. Remove and return the top item.

        An empty stack must raise IndexError with a message, not return None.
        A silent None is the bug that takes an hour to find later.
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Step 4. Return the top item without removing it.

        Same guard as pop. Read the last element, do not remove it.
        """
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Step 5. Return True when there is nothing on the stack."""
        return len(self._items) == 0

    def size(self):
        """Step 6. Return how many items are on the stack."""
        return len(self._items)

    def __len__(self):
        """Written for you, so len(stack) works once size() is done."""
        return self.size()