# Python eval() code injection
def calculate(expression):
    # EXTREMELY VULNERABLE: Arbitrary code execution
    result = eval(expression)
    return result

# User input: __import__('os').system('rm -rf /')
