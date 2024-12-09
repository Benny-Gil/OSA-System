document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/absences')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('history-container');
            data.forEach(absence => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                            <h2>${absence.date}</h2>
                            <p><strong>Reason:</strong> ${absence.reason}</p>
                            <p><strong>Course:</strong> ${absence.course}</p>
                            <p><strong>Status:</strong> ${absence.status}</p>
                        `;
                container.appendChild(card);
            });
        });
});