const form = document.querySelector('#generate-docstrings-form');
const codeInput = document.querySelector('#code-input');

form.addEventListener('submit', (e) => {
	e.preventDefault();

	const formData = new FormData();
	formData.append('code', codeInput.value);

	fetch('/generate_docstrings', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		codeInput.value = data.new_code;
		alert('Docstrings generated successfully!');
	})
	.catch(error => {
		alert('An error occurred while generating docstrings.');
		console.error(error);
	});
});
