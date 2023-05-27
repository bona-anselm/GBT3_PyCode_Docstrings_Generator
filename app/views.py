from flask import Blueprint
from flask import request, render_template


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    """
    Route handler for the home page.

    If the request method is POST, it extracts the code, function names, and class names
    from the form submission. Then, it generates docstrings for the functions and classes
    in the code and renders the index.html template with the updated code and docstrings.
    If the request method is GET, it simply renders the index.html template.

    Returns:
        str: The rendered HTML template.
    """
    from main import generate_docstrings

    if request.method == 'POST':
        code = request.form['code']
        functions = {}
        classes = {}
        for key, value in request.form.items():
            if key.startswith('function-'):
                functions[key.split('-')[1]] = value.strip()
            elif key.startswith('class-'):
                classes[key.split('-')[1]] = value.strip()

        results = generate_docstrings(code, functions, classes)

        return render_template('index.html', new_code=results['new_code'], docstrings=results['docstrings'])

    return render_template('index.html')
