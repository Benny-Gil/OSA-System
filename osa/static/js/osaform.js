function submitForm() {
    const formData = {
        date_absent: document.getElementById('date_absent').value,
        reason: document.getElementById('reason').value,
        course: document.getElementById('course').value
    };
    fetch('/add_student', {
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
            } else {
                const p = document.createElement('p');
                p.textContent = data[data.length - 1];
                resultsDiv.appendChild(p);
            }
        });
}

function goBack() {
    location.href = '/student';
}