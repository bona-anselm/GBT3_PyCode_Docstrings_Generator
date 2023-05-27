import ast
import astunparse
from app import create_app
from os import getenv
from app.models import ExtractClassNames, ExtractFunctionNames 
import openai


app = create_app()
openai.api_key = getenv('OPENAI_API_KEY')


def extract_names(code):
    """
    Extract function and class names from the code using AST.

    Args:
        code (str): The Python code to analyze.

    Returns:
        tuple: A tuple containing the extracted function names and class names.
    """
    tree = ast.parse(code)

    extract_functions = ExtractFunctionNames()
    extract_functions.visit(tree)

    extract_classes = ExtractClassNames()
    extract_classes.visit(tree)

    return extract_functions.function_names, extract_classes.class_names


def generate_docstring(prompt):
    """
    Generate a docstring using OpenAI API.

    Args:
        prompt (str): The prompt text for generating the docstring.

    Returns:
        str: The generated docstring.
    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def generate_docstrings(code, functions, classes):
    """Generates docstrings for functions and classes in the given code.

    Args:
        code (str): The Python code.
        functions (dict): A dictionary of function names and their corresponding docstrings.
        classes (dict): A dictionary of class names and their corresponding docstrings.

    Returns:
        dict: A dictionary containing the generated docstrings and the modified code with added docstrings.
    """
    function_names, class_names = extract_names(code)

    prompt = f"""Given the following code:

{code}

Please provide docstrings for the following functions and classes:"""

    for function_name in function_names:
        prompt += f"""

Function: {function_name}
Docstring: """

    for class_name in class_names:
        prompt += f"""

Class: {class_name}
Docstring: """

    docstrings = {}

    for function_name in function_names:
        docstring = functions.get(function_name)
        if docstring:
            docstrings[function_name] = docstring
        else:
            docstrings[function_name] = generate_docstring(prompt)

    for class_name in class_names:
        docstring = classes.get(class_name)
        if docstring:
            docstrings[class_name] = docstring
        else:
            docstrings[class_name] = generate_docstring(prompt)

    try:
        parsed_code = ast.parse(code)
        for node in parsed_code.body:
            if isinstance(node, ast.FunctionDef) and node.name in docstrings:
                if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Str):
                    docstring_node = ast.Expr(ast.Str(docstrings[node.name]))
                    docstring_node.value.s = '"""' + docstring_node.value.s.strip('"""').strip("'") + '"""'  # Strip enclosing single quotes
                    node.body = [docstring_node] + node.body
            if isinstance(node, ast.ClassDef) and node.name in docstrings:
                if not node.body or not isinstance(node.body[0], ast.Expr) or not isinstance(node.body[0].value, ast.Str):
                    docstring_node = ast.Expr(ast.Str(docstrings[node.name]))
                    docstring_node.value.s = '"""' + docstring_node.value.s.strip('"""').strip("'") + '"""'  # Strip enclosing single quotes
                    new_body = [docstring_node] + node.body
                    node.body = new_body

        new_code = astunparse.unparse(parsed_code)
    except SyntaxError:
        print("Error: could not parse code")

    return {"docstrings": docstrings, "new_code": new_code}



if __name__ == "__main__":
    app.run(debug=True)