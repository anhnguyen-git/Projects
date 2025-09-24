# Example Python file with various problems for testing the analyzer

import os
# Missing import for numpy but using np below

def badly_formatted_function(parameter_one, parameter_two, parameter_three, parameter_four, parameter_five):
    """This line is way too long and exceeds the recommended 88 character limit which makes it hard to read"""
    
    # TODO: Fix this function implementation
    print("Debug message")  # Should use logging instead
    
    # Using numpy without proper import
    result = np.array([1, 2, 3, 4, 5])
    
    # This line is extremely long and should be broken up into multiple lines for better readability and maintainability
    very_long_variable_name = parameter_one + parameter_two + parameter_three + parameter_four + parameter_five
    
    return result

# Syntax error on next line (missing colon)
def broken_function()
    return "This will cause a syntax error"

class ExampleClass:
    def __init__(self):
        print("Constructor called")  # Another print statement
        # FIXME: Implement proper initialization
        pass