function submitLogin() {
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            if (data.error) {
                const p = document.createElement('p');
                p.textContent = data.error;
                resultsDiv.appendChild(p);
            } else if (data.redirect) {
                window.location.href = data.redirect;
            }
        });
}