# Usage Examples

This document provides practical examples of using pylsp-rope's refactoring features.

## Basic Usage Patterns

Most refactoring operations follow this pattern:
1. Position your cursor on the target code
2. Trigger Code Action in your editor (typically `Ctrl+.` or `Cmd+.`)
3. Select the desired refactoring from the menu
4. Confirm any prompts or provide additional information

## Extract Method Examples

### Simple Method Extraction

**Before:**
```python
def calculate_total(items):
    subtotal = 0
    for item in items:
        subtotal += item.price * item.quantity
    tax = subtotal * 0.08
    return subtotal + tax
```

After selecting the tax calculation and triggering "Extract method":

**After:**
```python
def calculate_total(items):
    subtotal = 0
    for item in items:
        subtotal += item.price * item.quantity
    total_with_tax = add_tax(subtotal)
    return total_with_tax

def add_tax(subtotal):
    tax = subtotal * 0.08
    return subtotal + tax
```

### Method with Similar Statements

When similar statements exist, choose "Extract method including similar statements":

**Before:**
```python
def process_orders(orders):
    for order in orders:
        if order.status == "pending":
            total = sum(item.price for item in order.items)
            total = total * 1.1  # Add tax
            order.total = total

def process_invoices(invoices):
    for invoice in invoices:
        if invoice.status == "unpaid":
            total = sum(line.amount for line in invoice.lines)
            total = total * 1.1  # Add tax
            invoice.total = total
```

**After (including similar statements):**
```python
def process_orders(orders):
    for order in orders:
        if order.status == "pending":
            order.total = calculate_tax_total(item.price for item in order.items)

def process_invoices(invoices):
    for invoice in invoices:
        if invoice.status == "unpaid":
            invoice.total = calculate_tax_total(line.amount for line in invoice.lines)

def calculate_tax_total(amounts):
    total = sum(amounts)
    total = total * 1.1  # Add tax
    return total
```

## Extract Variable Examples

### Complex Expression

**Before:**
```python
def calculate_area(shape):
    return math.sqrt((shape.x2 - shape.x1) ** 2 + (shape.y2 - shape.y1) ** 2) * 0.5
```

After selecting the distance calculation:

**After:**
```python
def calculate_area(shape):
    distance = math.sqrt((shape.x2 - shape.x1) ** 2 + (shape.y2 - shape.y1) ** 2)
    return distance * 0.5
```

## Inline Examples

### Inline Variable

**Before:**
```python
def get_price(item):
    discounted_price = item.price * 0.9
    return discounted_price
```

After triggering "Inline" on `discounted_price`:

**After:**
```python
def get_price(item):
    return item.price * 0.9
```

### Inline Method

**Before:**
```python
def validate_email(email):
    return "@" in email and "." in email

def process_user(user):
    if validate_email(user.email):
        send_email(user.email)
```

After triggering "Inline" on the `validate_email` call:

**After:**
```python
def process_user(user):
    if "@" in user.email and "." in user.email:
        send_email(user.email)
```

## Use Function Examples

### Duplicated Code

**Before:**
```python
def calculate_circle_area(radius):
    result = math.pi * radius ** 2
    print(f"Calculated: {result}")
    return result

def calculate_square_area(side):
    result = side ** 2
    print(f"Calculated: {result}")
    return result

def calculate_triangle_area(base, height):
    result = 0.5 * base * height
    print(f"Calculated: {result}")
    return result
```

After selecting one of the similar blocks and using "Use function":

**After:**
```python
def calculate_and_log(calculation):
    result = calculation
    print(f"Calculated: {result}")
    return result

def calculate_circle_area(radius):
    return calculate_and_log(math.pi * radius ** 2)

def calculate_square_area(side):
    return calculate_and_log(side ** 2)

def calculate_triangle_area(base, height):
    return calculate_and_log(0.5 * base * height)
```

## Method to Method Object Examples

### Complex Method

**Before:**
```python
class ReportGenerator:
    def generate_complex_report(self, data):
        # Multiple steps with intermediate state
        filtered_data = [item for item in data if item.is_valid()]
        processed_data = []
        totals = {"count": 0, "sum": 0}

        for item in filtered_data:
            processed = self.process_item(item)
            processed_data.append(processed)
            totals["count"] += 1
            totals["sum"] += processed.value

        summary = self.create_summary(totals)
        return {
            "data": processed_data,
            "summary": summary
        }
```

After triggering "To method object":

**After:**
```python
class GenerateComplexReport:
    def __init__(self, data):
        self.data = data
        self.filtered_data = None
        self.processed_data = None
        self.totals = None
        self.summary = None

    def __call__(self):
        self.filter_data()
        self.process_data()
        self.calculate_totals()
        self.create_summary()
        return {
            "data": self.processed_data,
            "summary": self.summary
        }

    def filter_data(self):
        self.filtered_data = [item for item in self.data if item.is_valid()]

    def process_data(self):
        self.processed_data = []
        for item in self.filtered_data:
            processed = self.process_item(item)
            self.processed_data.append(processed)

    def calculate_totals(self):
        self.totals = {"count": 0, "sum": 0}
        for processed in self.processed_data:
            self.totals["count"] += 1
            self.totals["sum"] += processed.value

    def create_summary(self):
        self.summary = self.create_summary(self.totals)

class ReportGenerator:
    def generate_complex_report(self, data):
        return GenerateComplexReport(data)()
```

## Convert Local Variable to Field Examples

**Before:**
```python
class OrderProcessor:
    def process_single_order(self, order):
        customer_discount = self.get_customer_discount(order.customer_id)
        order_total = order.amount * (1 - customer_discount)
        return order_total

    def process_batch(self, orders):
        total = 0
        for order in orders:
            customer_discount = self.get_customer_discount(order.customer_id)
            total += order.amount * (1 - customer_discount)
        return total
```

After selecting `customer_discount` in the first method and using "Convert local variable to field":

**After:**
```python
class OrderProcessor:
    def process_single_order(self, order):
        self.customer_discount = self.get_customer_discount(order.customer_id)
        order_total = order.amount * (1 - self.customer_discount)
        return order_total

    def process_batch(self, orders):
        total = 0
        for order in orders:
            customer_discount = self.get_customer_discount(order.customer_id)
            total += order.amount * (1 - customer_discount)
        return total
```

## Introduce Parameter Examples

**Before:**
```python
class Logger:
    def __init__(self):
        self.level = "INFO"

    def log_message(self, message):
        print(f"[{self.level}] {message}")

def main():
    logger = Logger()
    logger.log_message("Starting process")
    logger.log_message("Process complete")
```

After selecting `self.level` in the log_message method and using "Introduce parameter":

**After:**
```python
class Logger:
    def __init__(self):
        self.level = "INFO"

    def log_message(self, message, level="INFO"):
        print(f"[{level}] {message}")

def main():
    logger = Logger()
    logger.log_message("Starting process", logger.level)
    logger.log_message("Process complete", logger.level)
```

## Generate Code Examples

### Generate Variable

**Before:**
```python
def main():
    print(user_name)
```

After triggering "Generate variable" on `user_name`:

**After:**
```python
def main():
    user_name = None
    print(user_name)
```

### Generate Function

**Before:**
```python
def main():
    result = calculate_something(5, 10)
    print(result)
```

After triggering "Generate function" on `calculate_something`:

**After:**
```python
def calculate_something(a, b):
    pass

def main():
    result = calculate_something(5, 10)
    print(result)
```

### Generate Class

**Before:**
```python
def main():
    user = User("John", "Doe")
    print(user.get_full_name())
```

After triggering "Generate class" on `User`:

**After:**
```python
class User:
    def __init__(self, arg1, arg2):
        pass

    def get_full_name(self):
        pass

def main():
    user = User("John", "Doe")
    print(user.get_full_name())
```

## Editor-Specific Shortcuts

### Vim/Neovim
```vim
" Trigger code actions
nnoremap <silent> <C-.> <cmd>lua vim.lsp.buf.code_action()<cr>
" Show available code actions
nnoremap <silent> <leader>ca <cmd>lua vim.lsp.buf.code_action()<cr>
```

### VS Code
- `Ctrl+.` (Windows/Linux)
- `Cmd+.` (macOS)
- Right-click → "Refactor"

### Emacs
```elisp
" Trigger code actions
(define-key lsp-mode-map (kbd "C-c C-r") 'lsp-execute-code-action)
```

These examples should help you understand how to effectively use pylsp-rope's refactoring capabilities in your development workflow.
