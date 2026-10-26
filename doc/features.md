# Features Overview

This document provides detailed information about all features available in pylsp-rope.

## Rename Features

### Current Capabilities
- ✅ **Variables**: Rename local and global variables
- ✅ **Classes**: Rename class definitions and their usages
- ✅ **Functions**: Rename function definitions and calls
- ❌ **Modules**: Move and rename module files (planned)
- ❌ **Packages**: Move and rename package directories (planned)

### Rename Behavior
When Rename is triggered on a symbol under the cursor:

1. **Variables, Classes, Functions**: Renames all occurrences across the project
2. **Modules/Packages** (future): Will move files and update all import statements

## Code Actions

### Extract Method

**Variants:**
- Extract method
- Extract global method
- Extract method including similar statements
- Extract global method including similar statements

**Usage:** Trigger CodeAction on any code block to extract it into a method. Similar statements can optionally be extracted as well.

**Example:**
```python
# Before
def process_data(data):
    result = data * 2
    result = result + 10
    return result

# After extracting "result = result + 10"
def process_data(data):
    result = data * 2
    result = add_offset(result)
    return result

def add_offset(value):
    return value + 10
```

### Extract Variable

**Variants:**
- Extract variable
- Extract global variable
- Extract variable including similar statements
- Extract global variable including similar statements

**Usage:** Trigger CodeAction on an expression to extract it into a variable. Similar statements can optionally be extracted as well.

**Example:**
```python
# Before
def calculate(a, b):
    return a * 2 + b * 2

# After extracting "a * 2" into "doubled_a"
def calculate(a, b):
    doubled_a = a * 2
    return doubled_a + b * 2
```

### Inline

**Usage:** Trigger CodeAction on a resolvable variable or method to replace all calls with the actual implementation.

**Example:**
```python
# Before
def helper(x):
    return x * 2

def calculate():
    result = helper(5)
    return result

# After inlining helper()
def calculate():
    result = 5 * 2
    return result
```

### Use Function

**Usage:** Trigger CodeAction on a function name to replace code matching the function's body with a call to that function.

**Example:**
```python
# Before
def calculate():
    a = 5
    b = a * 2
    return b

def another_function():
    x = 10
    y = x * 2
    return y

# After using calculate() for the duplicated code
def calculate():
    a = 5
    b = calculate()
    return b

def another_function():
    x = 10
    y = calculate()
    return y
```

### Method to Method Object

**Usage:** Trigger CodeAction on a method to create a callable class that replaces that method. This is useful for complex methods that need to be converted to objects.

**Example:**
```python
# Before
class Calculator:
    def complex_calculation(self, x, y):
        # complex logic here
        intermediate = x + y
        result = intermediate * 2
        return result

# After
class ComplexCalculation:
    def __call__(self, x, y):
        intermediate = x + y
        result = intermediate * 2
        return result

class Calculator:
    def complex_calculation(self, x, y):
        return ComplexCalculation()(x, y)
```

### Convert Local Variable to Field

**Usage:** Trigger CodeAction on a local variable inside a method to convert it to a class attribute.

**Example:**
```python
# Before
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        local_count = self.count + 1
        self.count = local_count

# After
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count = self.count + 1
```

### Organize Imports

**Usage:** Trigger CodeAction anywhere in a Python file to clean up import statements:
- Remove unused imports
- Sort imports alphabetically
- Group imports by type (standard library, third-party, local)

### Introduce Parameter

**Usage:** Trigger CodeAction while selecting a variable or attribute to make it a method parameter.

**Example:**
```python
# Before
class Greeter:
    def __init__(self):
        self.name = "World"

    def greet(self):
        return f"Hello, {self.name}!"

# After introducing parameter
class Greeter:
    def __init__(self):
        self.name = "World"

    def greet(self, name):
        return f"Hello, {name}!"
```

### Generate Code

**Variants:**
- ✅ Generate variable
- ✅ Generate function
- ✅ Generate class
- ❌ Generate module (planned)
- ❌ Generate package (planned)

**Usage:** Trigger CodeAction on an undefined variable to generate an empty definition.

**Example:**
```python
# Before
def main():
    result = calculate_something(5, 10)
    print(result)

# After generating calculate_something
def calculate_something(a, b):
    pass

def main():
    result = calculate_something(5, 10)
    print(result)
```

## Refactoring Safety

All refactorings use Rope's sophisticated analysis engine to:
- Preserve code semantics
- Handle cross-file dependencies
- Maintain proper scoping
- Update import statements as needed
- Handle complex inheritance hierarchies

## Limitations

- Support for unsaved documents is experimental
- Module and package renaming is not yet implemented
- Some complex refactorings may require manual intervention
- Performance may vary with very large codebases
