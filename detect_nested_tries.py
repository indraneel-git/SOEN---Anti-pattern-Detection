import os
import ast

input_directory = 'C:\\Users\\kosur\\OneDrive\\Desktop\\assignment presentation\\Python-calculus\\calculus'

# Define a function called find_python_files that takes a directory path as input
def find_python_files(directory):
    # Create an empty list called python_files
    python_files = []
    # Use the os.walk method to iterate through all the directories and files in the input directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        # Iterate through each file in the current directory
        for file in files:
            # If the file ends with '.py', append its full path to the python_files list
           
            if file.endswith('.py'):
                print(file)
                python_files.append(os.path.join(root, file))
    # Return the python_files list
    return python_files

#This function named is_try takes an AST node as input and returns True if the node represents a try statement in Python code, and False otherwise. The implementation of the function uses the isinstance() built-in function to check whether the input node is an instance of the ast.Try class, which represents a try statement in Python's abstract syntax tree (AST).
def is_try(node):
    return isinstance(node, ast.Try)

#This function named find_nested_tries takes three arguments: an AST node representing the root of the AST, a filename (as a string), and a set of line numbers. The function recursively walks through the AST, looking for nested try statements within the try blocks and except blocks.

#The implementation of the function first checks if the input node represents a try statement, by calling the is_try function. If the node is a try statement, the function iterates through its body and handlers, looking for nested try statements. If a nested try statement is found, its line number is added to the set of line numbers.
def find_nested_tries(node, filename, line_numbers):
    if is_try(node):
    
        for nested_node in node.body:
            if is_try(nested_node):
                line_numbers.add(nested_node.lineno)
        for handler in node.handlers:
            for nested_node in handler.body:
                if is_try(nested_node):
                    line_numbers.add(nested_node.lineno)
    for child_node in ast.iter_child_nodes(node):
        find_nested_tries(child_node, filename, line_numbers)

#The following code first finds all Python files in the input_directory and stores them in the python_files list using the find_python_files function.

#Then, the code creates an empty dictionary called results.

#For each file in python_files, the code opens the file and attempts to parse it using the ast.parse function. If the file cannot be parsed due to a syntax error, the code moves on to the next file.

#If the file is successfully parsed, the code calls the find_nested_tries function with the parsed AST, file name, and an empty set called nested_tries.

#find_nested_tries recursively traverses the AST and looks for try nodes. If a try node is found, it looks for nested try nodes inside its body and handlers. If any nested try nodes are found, their line numbers are added to the nested_tries set.

#After the find_nested_tries function completes, the code checks if the nested_tries set is not empty. If there are nested try nodes in the file, the file name and line numbers of the nested try nodes are added to the results dictionary.

#Finally, the results directory contains the file names and line numbers of all Python files in the input_directory that contain nested try blocks.
python_files = find_python_files(input_directory)

results = {}
for file in python_files:
    with open(file, 'r') as f:
        try:
            tree = ast.parse(f.read())
            nested_tries = set()
            find_nested_tries(tree, file, nested_tries)
            if nested_tries:
                results[file] = nested_tries
        except SyntaxError:
            pass

#The following code opens a file called output.txt in write mode and uses a with statement to ensure that the file is properly closed when the block is exited.

#The code then iterates through the items in the results dictionary, which contains the file names and line numbers of all Python files in the input_directory that contain nested try blocks.

#For each file in results, the code writes the file name to the output.txt file, followed by a colon and a newline character.

#Next, the code iterates through the line numbers associated with the current file and writes each line number preceded by the text "Line" and a tab character to the output.txt file.

#After writing all of the line numbers for the current file, the code writes the total number of nested try blocks found in the file, preceded by the text "Total nested try blocks:" and a newline character, to the output.txt file.

#Finally, when all files have been processed, the output.txt file contains a summary of all Python files in the input_directory that contain nested try blocks, including the file name, line numbers, and total number of nested try blocks.
with open('output.txt', 'w') as f:
    for filename, line_numbers in results.items():
        f.write(f'{filename}:\n')
        for line_number in line_numbers:
            f.write(f'\tLine {line_number}\n')
        f.write(f'\tTotal nested try blocks: {len(line_numbers)}\n')
