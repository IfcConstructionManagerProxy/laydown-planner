class Object:
    def __init__(self, name, weight, dimensions):
        self.name = name
        self.weight = weight  # in kilograms
        self.dimensions = dimensions  # (length, width, height)

class Stack:
    def __init__(self):
        self.items = []
        self.total_weight = 0

    def add(self, obj):
        self.items.append(obj)
        self.total_weight += obj.weight

    def can_stack(self, obj):
        # Implement stackability rules and constraints here
        # Example: Check weight limit or dimension compatibility
        return True  # Placeholder for actual logic

    def stack(self, obj):
        if self.can_stack(obj):
            self.add(obj)
        else:
            raise ValueError("Cannot stack object: violates stackability rules")
