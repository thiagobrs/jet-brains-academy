# import the necessary packages
import os
import sys
import glob
import re
import ast
from typing import Tuple


class MaxLineLengthError(Exception):
    """Return the error code and description when a line exceeds the max line length according to PEP8."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S001"
        self.message = "Too long"
        super().__init__(f"{self.code} {self.message}")


class InvalidIndentationError(Exception):
    """Return the error code and description when the number of indentation spaces is not a multiple of 4."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S002"
        self.message = "Invalid indentation"
        super().__init__(f"{self.code} {self.message}")


class UnnecessarySemicolonError(Exception):
    """Return the error code and description when there is a semicolon after a statement."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S003"
        self.message = "Unnecessary semicolon"
        super().__init__(f"{self.code} {self.message}")


class InlineCommentSpaceError(Exception):
    """Return the error code and description when there are less than 2 spaces before inline comments."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S004"
        self.message = "At least two spaces required before inline comments"
        super().__init__(f"{self.code} {self.message}")


class TodoInCommentError(Exception):
    """Return the error code and description when a TO DO is found in a  comment."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S005"
        self.message = "TODO found"
        super().__init__(f"{self.code} {self.message}")


class MaxBlankLinesError(Exception):
    """Return the error code and description when more than 2 blank lines were found before a code line."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S006"
        self.message = "More than two blank lines used before this line"
        super().__init__(f"{self.code} {self.message}")


class ConstructionSpacesError(Exception):
    """Return the error code and description when there is more than 1 space after the construction_name."""

    def __init__(self, construction_name: str):
        """The initializer for the class, define the error code and the error message.

        Keyword arguments:
        construction_name -- Name of the construction (def or class)
        """

        self.code = "S007"
        self.message = f"Too many spaces after '{construction_name}'"
        super().__init__(f"{self.code} {self.message}")


class ClassNameError(Exception):
    """Return the error code and description when a class name is not in CamelCase."""

    def __init__(self, class_name: str):
        """The initializer for the class, define the error code and the error message.

        Keyword arguments:
        class_name -- Name of the class
        """

        self.code = "S008"
        self.message = f"Class name '{class_name}' should use CamelCase"
        super().__init__(f"{self.code} {self.message}")


class FunctionNameError(Exception):
    """Return the error code and description when a function name is not in snake_case."""

    def __init__(self, function_name: str):
        """The initializer for the class, define the error code and the error message.

        Keyword arguments:
        function_name -- Name of the function
        """

        self.code = "S009"
        self.message = f"Function name '{function_name}' should use snake_case"
        super().__init__(f"{self.code} {self.message}")


class FunctionArgNameError(Exception):
    """Return the error code and description when a function argument name is not in snake_case."""

    def __init__(self, argument_name: str):
        """The initializer for the class, define the error code and the error message.

        Keyword arguments:
        argument_name -- Name of the function argument
        """

        self.code = "S010"
        self.message = f"Argument name '{argument_name}' should be snake_case"
        super().__init__(f"{self.code} {self.message}")


class FunctionVarNameError(Exception):
    """Return the error code and description when a variable name inside a function is not in snake_case."""

    def __init__(self, variable_name: str):
        """The initializer for the class, define the error code and the error message.

        Keyword arguments:
        variable_name -- Name of the variable
        """

        self.code = "S011"
        self.message = f"Variable '{variable_name}' in function should be snake_case"
        super().__init__(f"{self.code} {self.message}")


class FunctionArgMutableError(Exception):
    """Return the error code and description when a function argument has mutable objects as default values."""

    def __init__(self):
        """The initializer for the class, define the error code and the error message."""

        self.code = "S012"
        self.message = f"Default argument value is mutable"
        super().__init__(f"{self.code} {self.message}")


class StaticCodeAnalyzer:
    """Represents a static code analyzer for a single files or a directory."""

    # Class variables
    MAX_LINE_LENGTH = 79
    INDENTATION_SIZE = 4
    MIN_INLINE_COMMENT_SPACE = 2
    MAX_BLANK_LINES = 2

    def __init__(self):
        """The initializer for the class."""

        self.file_name = ""
        self.code_text = []

    def load_file(self, file_name: str):
        """Check if the file exists and loads it.

        Keyword arguments:
        file_name -- Full name of the file to read from
        """

        try:
            # Try to open the file
            f = open(file_name, "r", encoding='utf-8')
        except OSError:
            # If an error occur, show a message
            print("Error: Could not open file: ", file_name)
        else:
            with f:
                # Update the instance file_name attribute
                self.file_name = file_name

                # Update the code_text attribute with the list of lines of the file
                self.code_text = f.readlines()

    def check_line_length(self, line: Tuple):
        """Check if the line length is according to PEP8 (max 79 characters).

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """

        try:
            if len(line[1]) > self.MAX_LINE_LENGTH:
                raise MaxLineLengthError
        except MaxLineLengthError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_indentation(self, line: Tuple):
        """Check if the number of indentation spaces is according to PEP8 (multiple of 4).

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """

        try:
            # Detect if there is one or more spaces in the beginning of the line
            pattern = r"^ +"
            match = re.match(pattern, line[1])

            # Check if the number of spaces is a multiple of 4
            if match and (len(match.group()) % self.INDENTATION_SIZE) != 0:
                raise InvalidIndentationError
        except InvalidIndentationError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_semicolons(self, line: Tuple):
        """Check if the number of indentation spaces is according to PEP8 (multiple of 4).

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """

        try:
            # Detect a semicolon in the end of the line, followed or not by an inline comment
            pattern = r";\s*$|;(\s*#.*)?$"
            if re.search(pattern, line[1]):
                # Detect if the semicolon is inside an inline comment
                pattern = r"#.*;\s*$"
                if not re.search(pattern, line[1]):
                    raise UnnecessarySemicolonError
        except UnnecessarySemicolonError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_comment_spaces(self, line: Tuple):
        """Check if the number of spaces before inline comments is according to PEP8 (min 2).

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """

        try:
            pattern_1 = r"^.+\S ?#"  # Detect an inline comment with less than 2 spaces to the code
            pattern_2 = r" {2}#.*#"  # Detect if the # is inside an inline comment
            if re.search(pattern_1, line[1]) and not re.search(pattern_2, line[1]):
                raise InlineCommentSpaceError
        except InlineCommentSpaceError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_todo_comments(self, line: Tuple):
        """Check if there are TODOs inside comments.

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """
        try:
            # Detect a TO DO inside an inline comment
            pattern = r"#.* (todo)( .*)?$"
            if re.search(pattern, line[1], flags=re.IGNORECASE):
                raise TodoInCommentError
        except TodoInCommentError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_blank_lines(self, line: Tuple, blank_count: int):
        """Check if more than 2 blank lines were found before a code line.

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        blank_count -- Number of consecutive blank lines detected
        """

        try:
            if blank_count > self.MAX_BLANK_LINES and len(line[1].strip()) > 0:
                raise MaxBlankLinesError
        except MaxBlankLinesError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_construction_spaces(self, line: Tuple):
        """Check if the number of spaces after a construction name is according to PEP8 (max 1).

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """

        try:
            # Detect more than 1 space after a construction_name
            pattern = r"^ *(def|class) {2,}"
            match = re.search(pattern, line[1])
            if match:
                raise ConstructionSpacesError(match.group().strip())
        except ConstructionSpacesError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_class_name(self, line: Tuple):
        """Check if a given class name is in CamelCase.

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        """

        try:
            # Detect if a class_name is not in CamelCase
            pattern = r"\b(?<=class) +([a-z_]\w*|\w*_\w*)"
            match = re.search(pattern, line[1])

            if match:
                raise ClassNameError(match.group().strip())
        except ClassNameError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_function_name(self, line: Tuple):
        """Check if a given function name is in snake_case.

        Keyword arguments:
        line -- Tuple that represents one line of the file (line_number, text)
        function_name -- The name of the function to analyse
        """

        try:
            # Detect if a function_name is not in snake_case
            pattern = r"\b(?<=def) +([A-Z]*\w*[A-Z]\w*)"
            match = re.search(pattern, line[1])
            if match:
                raise FunctionNameError(match.group().strip())
        except FunctionNameError as err:
            print(f"{self.file_name}: Line {line[0]}: {err}")

    def check_function_args_names(self, node):
        """Check if a given function name is in snake_case.

        Keyword arguments:
        line_number -- Number of the line in the code
        node -- AST tree object of the function
        """

        try:
            args = [a.arg for a in node.args.args]
            for arg in args:
                # Detect if arg_name is not in snake_case
                pattern = r"[A-Z]*\w*[A-Z]\w*"
                match = re.search(pattern, arg)
                if match:
                    raise FunctionArgNameError(arg)
        except FunctionArgNameError as err:
            print(f"{self.file_name}: Line {node.lineno}: {err}")

    def check_function_args_mutable(self, node):
        """Check if a given function name is in snake_case.

        Keyword arguments:
        line_number -- Number of the line in the code
        node -- AST tree object of the function
        """

        try:
            for arg in node.args.defaults:
                # Detect if arg_name is not in snake_case
                if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                    raise FunctionArgMutableError()
        except FunctionArgMutableError as err:
            print(f"{self.file_name}: Line {node.lineno}: {err}")

    def check_function_var_names(self, node):
        """Check if variables names inside functions are in snake_case.

        Keyword arguments:
        line_number -- Number of the line in the code
        node -- AST tree object of the function
        """

        # Create a list of tuples with all names and line numbers of variables in the function
        # var_names = [(a.targets[0].id, a.lineno) for a in node.body if isinstance(a, ast.Assign)]
        var_names = []
        for a in node.body:
            if isinstance(a, ast.Assign):
                if isinstance(a.targets[0], ast.Name):
                    var_names.append((a.targets[0].id, a.lineno))
                elif isinstance(a.targets[0], ast.Attribute):
                    var_names.append((a.targets[0].attr, a.lineno))

        # Set used to avoid analyzing the same variable in different assignment statements
        var_checked = set()

        # Iterate over each (variable name, line number) tuple
        for var_name in var_names:
            try:
                # If the variable wasn't analyzed yet...
                if var_name[0] not in var_checked:
                    # Detect if var_name is not in snake_case
                    pattern = r"[A-Z]*\w*[A-Z]\w*"
                    match = re.search(pattern, var_name[0])
                    if match:
                        # Update the checked variables set
                        var_checked.add(var_name[0])
                        raise FunctionVarNameError(var_name[0])
            except FunctionVarNameError as err:
                print(f"{self.file_name}: Line {var_name[1]}: {err}")

    def check_function_definition(self):
        """Check if functions arguments are mutable and if functions args and variables names are in snake_case"""
        try:
            with open(self.file_name, "r") as source:
                tree = ast.parse(source.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.check_function_args_names(node)
                    self.check_function_args_mutable(node)
                    self.check_function_var_names(node)
        finally:
            # If any syntax or semantic error occur while parsing, ignore
            pass

    def analyze_file(self, file_name: str):
        """Analyze the code of a given file according to PEP8.

        Keyword arguments:
        file_name -- Full name of the file to read from
        test_mode -- Flag that indicates if the program is executing on test mode
        """

        # Load the file content
        self.load_file(file_name)

        # Initialize the blank line count
        blank_count = 0

        # Walk through the python file to check functions args and variables
        self.check_function_definition()

        # Iterate over each line of the file
        for line in enumerate(self.code_text, 1):
            # Execute the analyzing methods over the current line
            self.check_line_length(line)
            self.check_indentation(line)
            self.check_semicolons(line)
            self.check_comment_spaces(line)
            self.check_todo_comments(line)
            self.check_blank_lines(line, blank_count)
            self.check_construction_spaces(line)
            self.check_class_name(line)
            self.check_function_name(line)

            # If a blank line was found, update the blank line count
            if line[1].strip() == '':
                blank_count += 1
            # Otherwise, reset it to zero
            else:
                blank_count = 0

    def analyze_path(self, path_name: str):
        """Analyze the code of the Python files in a given directory according to PEP8.

        Keyword arguments:
        path_name -- Full name of the directory where the Python files should be
        test_mode -- Flag that indicates if the program is executing on test mode
        """

        # Analyze each Python file in the given directory
        for file_name in glob.glob(path_name + "/*.py"):
            self.analyze_file(file_name)


def main():
    """Call the appropriate validation method according to the arguments."""

    test_mode = False

    if test_mode:
        static_code_analyzer = StaticCodeAnalyzer()
        static_code_analyzer.analyze_file('test_file.py')
    else:
        # Get the command line arguments
        args = sys.argv

        # Check if exactly one argument was informed
        if len(args) == 2:
            static_code_analyzer = StaticCodeAnalyzer()

            # Call the appropriate analysis method according to the argument type: file or directory
            if os.path.isdir(args[1]):
                static_code_analyzer.analyze_path(args[1])
            elif args[1].endswith(".py"):
                static_code_analyzer.analyze_file(args[1])

        elif len(args) > 2:
            print("Too many arguments.")
        else:
            print("No argument was informed.")


if __name__ == "__main__":
    main()
