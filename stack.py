from datetime import datetime


class ExpirationStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        """
        Pushes an item (name, expiration_date) into the stack.
        The stack is maintained in order of nearest to farthest expiration date.
        """
        if not isinstance(item['expiration_date'], datetime):
            raise ValueError("expiration_date must be a datetime object")

        inserted = False
        for i in range(len(self.stack)):
            if item['expiration_date'] < self.stack[i]['expiration_date']:
                self.stack.insert(i, item)
                inserted = True
                break
        if not inserted:
            self.stack.append(item)

    def pop(self):
        """Removes and returns the top item (nearest expiration date)."""
        if self.is_empty():
            return None
        return self.stack.pop(0)

    def peek(self):
        """Returns the top item without removing it."""
        if self.is_empty():
            return None
        return self.stack[0]

    def is_empty(self):
        """Checks if the stack is empty."""
        return len(self.stack) == 0

    def get_stack(self):
        """Returns the entire stack (for viewing or debugging)."""
        return self.stack


# Example Usage
stack = ExpirationStack()

# Add items with expiration dates
stack.push({"name": "Milk", "expiration_date": datetime(2024, 11, 18)})
stack.push({"name": "Bread", "expiration_date": datetime(2024, 11, 15)})
stack.push({"name": "Cheese", "expiration_date": datetime(2024, 12, 1)})

# Check the stack
print("Stack after pushes:", stack.get_stack())

# Peek the nearest expiration
print("Top item (nearest expiration):", stack.peek())

# Pop the top item
print("Popped item:", stack.pop())

# Check the stack again
print("Stack after pop:", stack.get_stack())