# Revised Implementation of a CLI Scientific Calculator using Sympy

"""
Overview:
This file contains the implementation of a command-line interface (CLI) scientific calculator.
The calculator is capable of evaluating symbolic mathematical expressions using the Sympy library.
It supports two modes: a Read-Eval-Print Loop (REPL) mode for interactive input and a command-line mode
for single expression evaluation.

Modules and Functions:
1. Command-line argument parsing to determine the mode of operation.
2. Expression evaluation using Sympy.
3. REPL implementation for interactive mode.
4. Error handling and user-friendly output.

Dependencies:
- Sympy for symbolic mathematics.
- Argparse for command-line argument parsing.
"""

import sys
import sympy as sp
import argparse

# Function to evaluate mathematical expressions using Sympy
def evaluate_expression(expression):
    """
    Parses and evaluates a mathematical expression using Sympy.
    
    :param expression: A string containing the mathematical expression to evaluate.
    :return: The evaluated result of the expression or an error message.
    """
    try:
        # Parse the expression using sympy
        expr = sp.sympify(expression, evaluate=False)
        # Evaluate the expression
        result = sp.simplify(expr)
        return result
    except sp.SympifyError:
        # Handle parsing errors and return a user-friendly message
        return "Error: Invalid expression (could not parse the input as a valid mathematical expression)"
    except Exception as e:
        # Handle all other types of errors
        return f"Error: An unexpected error occurred ({str(e)})"

# Function to handle the REPL (Read-Eval-Print Loop) mode
def repl_mode():
    """
    Starts a Read-Eval-Print Loop (REPL) for interactive expression evaluation.
    """
    print("Sympy CLI Calculator REPL. Type 'exit' to quit.")
    while True:
        # Prompt user for input
        user_input = input(">>> ")
        # Check for exit command
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting REPL. Goodbye!")
            break

        # Evaluate the expression and print the result
        result = evaluate_expression(user_input)
        print(result)

# Function to parse command-line arguments and determine mode of operation
def parse_arguments():
    """
    Parses command-line arguments to determine if a single expression is being passed or if REPL mode should start.
    
    :return: Namespace object containing command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Sympy CLI Calculator")
    parser.add_argument('expression', nargs='?', help='Mathematical expression to evaluate')
    return parser.parse_args()

# Main entry point for the application
def main():
    """
    Main function for the CLI calculator application. Determines mode of operation based on command-line arguments.
    """
    args = parse_arguments()
    if args.expression:
        # Command-line mode: evaluate the provided expression
        result = evaluate_expression(args.expression)
        print(result)
    else:
        # Start REPL mode since no expression was provided
        repl_mode()

# Ensure the script runs as a standalone program
if __name__ == '__main__':
    main()

"""
Usage Instructions:
1. Run the script with a mathematical expression as an argument to evaluate it directly:
   python calculator.py "2 + 2"

2. Run the script without arguments to start the REPL mode:
   python calculator.py
   In REPL mode, type mathematical expressions and press Enter to evaluate them. Type 'exit' to quit.

Error Handling:
- The program displays an error message if an invalid expression is entered.

Testing:
- The functionality can be tested using different mathematical expressions to ensure accurate evaluation.
- Pytest can be employed to automate testing of different components.

Future Enhancements:
- Add more advanced mathematical functions and operations.
- Improve user interface with additional features like history of evaluated expressions.
"""

# Note: Additional import for sys in test cases is assumed to be fixed in the test suite where sys.argv is used.
# This code focuses on implementing the main functionality of the CLI calculator.